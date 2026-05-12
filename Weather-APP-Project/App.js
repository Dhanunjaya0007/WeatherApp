/* ════════════════════════════════════════════════
   WeatherGlass — app.js
   Frontend JS — talks to your Flask backend at
   http://localhost:5000/weather?city=CityName
   ════════════════════════════════════════════════ */

/* ──────────────────────────────
   CONFIG
   ────────────────────────────── */
const BACKEND_URL = "http://localhost:5000/weather";  // Flask backend endpoint


/* ──────────────────────────────
   DOM REFERENCES
   ────────────────────────────── */
const scene       = document.getElementById("scene");
const cityInput   = document.getElementById("city-input");
const submitBtn   = document.getElementById("submit-btn");
const errorMsg    = document.getElementById("error-msg");
const resultEl    = document.getElementById("result");
const weatherIcon = document.getElementById("weather-icon");
const statusDot   = document.getElementById("status-dot");
const statusText  = document.getElementById("status-text");


/* ──────────────────────────────
   ICON MAP
   weather_id ranges → emoji
   ────────────────────────────── */
function getIconAndScene(weatherId, temp) {
  if (weatherId >= 200 && weatherId < 300) return { icon: "⛈️",  scene: "stormy" };
  if (weatherId >= 300 && weatherId < 400) return { icon: "🌦️",  scene: "rainy"  };
  if (weatherId >= 500 && weatherId < 600) return { icon: "🌧️",  scene: "rainy"  };
  if (weatherId >= 600 && weatherId < 700) return { icon: "❄️",  scene: "snowy"  };
  if (weatherId >= 700 && weatherId < 800) return { icon: "🌫️",  scene: "foggy"  };
  if (weatherId === 800) {
    if (temp > 35) return { icon: "🌡️", scene: "hot"   };
    if (temp < 2)  return { icon: "🌙", scene: "night" };
    return             { icon: "☀️", scene: "sunny"  };
  }
  if (weatherId > 800) return { icon: "⛅",  scene: "cloudy" };
  return { icon: "🌤️", scene: "sunny" };
}


/* ──────────────────────────────
   APPLY SCENE
   ────────────────────────────── */
function applyScene(sceneName, icon) {
  scene.className  = sceneName;
  weatherIcon.textContent = icon;
}


/* ──────────────────────────────
   RENDER RESULT
   ────────────────────────────── */
function renderResult(data) {
  /*
    data shape (from Flask /weather endpoint):
    {
      city, country, temp, feels_like,
      humidity, wind_speed, description,
      weather_id, weather_main
    }
  */
  document.getElementById("r-city").textContent      = data.city;
  document.getElementById("result-country").textContent = data.country;
  document.getElementById("result-temp").textContent  = `${data.temp}°C`;
  document.getElementById("result-desc").textContent  = data.description;
  document.getElementById("r-humidity").textContent   = `${data.humidity}%`;
  document.getElementById("r-wind").textContent       = `${data.wind_speed} m/s`;
  document.getElementById("r-feels").textContent      = `${data.feels_like}°C`;

  // Determine scene and icon from weather ID + temp
  const { icon, scene: sceneName } = getIconAndScene(data.weather_id, data.temp);
  applyScene(sceneName, icon);

  resultEl.classList.add("visible");
}


/* ──────────────────────────────
   FETCH WEATHER FROM FLASK
   ────────────────────────────── */
async function fetchWeather(city) {
  errorMsg.textContent = "";

  if (!city) {
    errorMsg.textContent = "Please enter a city name.";
    return;
  }

  setLoading(true);

  try {
    // ── Hit our Flask backend (not OpenWeatherMap directly) ──
    const response = await fetch(`${BACKEND_URL}?city=${encodeURIComponent(city)}`);
    const data     = await response.json();

    if (data.error) {
      errorMsg.textContent = data.message || "Something went wrong.";
      return;
    }

    renderResult(data);

  } catch (err) {
    // Flask server not running
    errorMsg.textContent = "Cannot reach backend. Run: python server.py";
    setBackendStatus(false);
    console.error("Backend fetch error:", err);
  } finally {
    setLoading(false);
  }
}


/* ──────────────────────────────
   LOADING STATE
   ────────────────────────────── */
function setLoading(state) {
  submitBtn.classList.toggle("loading", state);
}


/* ──────────────────────────────
   BACKEND STATUS CHECKER
   Pings /weather every 10 sec
   ────────────────────────────── */
function setBackendStatus(online) {
  statusDot.className  = online ? "online" : "offline";
  statusText.textContent = online
    ? "Backend connected — live data"
    : "Backend offline — run python server.py";
}

async function checkBackend() {
  try {
    const res = await fetch(`${BACKEND_URL}?city=London`, { signal: AbortSignal.timeout(3000) });
    const data = await res.json();
    setBackendStatus(!data.error || data.message !== undefined); // got a response = server alive
  } catch {
    setBackendStatus(false);
  }
}

checkBackend();
setInterval(checkBackend, 10000);


/* ──────────────────────────────
   EVENTS
   ────────────────────────────── */
submitBtn.addEventListener("click", () => {
  fetchWeather(cityInput.value.trim());
});

cityInput.addEventListener("keydown", e => {
  if (e.key === "Enter") fetchWeather(cityInput.value.trim());
});

// Quick city pills
document.querySelectorAll(".quick-pill").forEach(pill => {
  pill.addEventListener("click", () => {
    const city = pill.dataset.city;
    cityInput.value = city;
    fetchWeather(city);
  });
});


/* ──────────────────────────────
   PARTICLE BUILDERS
   Runs once on page load
   ────────────────────────────── */
(function buildParticles() {

  // Sun rays
  const raysEl = document.getElementById("sun-rays");
  for (let i = 0; i < 12; i++) {
    const ray = document.createElement("div");
    ray.className = "ray";
    ray.style.cssText = `
      transform: rotate(${i * 30}deg) translateX(-50%);
      left: 50%; top: 50%;
      height: ${50 + Math.random() * 28}px;
    `;
    raysEl.appendChild(ray);
  }

  // Stars (90)
  const starsEl = document.getElementById("stars");
  for (let i = 0; i < 90; i++) {
    const s  = document.createElement("div");
    s.className = "star";
    const sz = 0.8 + Math.random() * 2.4;
    s.style.cssText = `
      width:${sz}px; height:${sz}px;
      left:${Math.random()*100}%; top:${Math.random()*65}%;
      --t:${2+Math.random()*4}s; --d:${Math.random()*5}s;
    `;
    starsEl.appendChild(s);
  }

  // Clouds (5 layers)
  const cloudsEl = document.getElementById("clouds");
  [
    { top:"7%",  w:220, h:60, dur:55, delay:0,  co:0.80 },
    { top:"14%", w:160, h:45, dur:70, delay:12, co:0.55 },
    { top:"22%", w:295, h:72, dur:40, delay:5,  co:0.65 },
    { top:"5%",  w:180, h:50, dur:80, delay:25, co:0.40 },
    { top:"18%", w:130, h:38, dur:60, delay:38, co:0.50 },
  ].forEach(c => {
    const cloud = document.createElement("div");
    cloud.className = "cloud";
    cloud.style.cssText = `
      top:${c.top}; width:${c.w}px; height:${c.h}px;
      --co:${c.co}; --from:-${c.w+20}px; --to:110vw;
      animation-duration:${c.dur}s; animation-delay:-${c.delay}s;
    `;
    cloudsEl.appendChild(cloud);
  });

  // Rain drops (90)
  const rainEl = document.getElementById("rain");
  for (let i = 0; i < 90; i++) {
    const drop = document.createElement("div");
    drop.className = "drop";
    drop.style.cssText = `
      left:${Math.random()*110-5}%;
      height:${10+Math.random()*24}px;
      opacity:${0.4+Math.random()*0.55};
      animation-duration:${0.45+Math.random()*0.6}s;
      animation-delay:-${Math.random()*1.5}s;
    `;
    rainEl.appendChild(drop);
  }

  // Snowflakes (55)
  const snowEl = document.getElementById("snow");
  ["❄","❅","❆","·","•"].forEach((shape, si) => {
    for (let i = 0; i < 11; i++) {
      const flake = document.createElement("div");
      flake.className  = "flake";
      flake.textContent = shape;
      const fs = 8 + Math.random() * 16;
      flake.style.cssText = `
        left:${Math.random()*105}%; font-size:${fs}px;
        opacity:${0.5+Math.random()*0.5};
        animation-duration:${4+Math.random()*6}s;
        animation-delay:-${Math.random()*8}s;
      `;
      snowEl.appendChild(flake);
    }
  });

  // Fog layers (5)
  const fogEl = document.getElementById("fog");
  [15, 28, 42, 56, 70].forEach((top, i) => {
    const layer = document.createElement("div");
    layer.className = "fog-layer";
    layer.style.cssText = `
      top:${top}%;
      animation-duration:${8+i*3}s;
      animation-delay:-${i*2}s;
      opacity:${0.55+i*0.05};
    `;
    fogEl.appendChild(layer);
  });

})();