// World Bio-Optimum Index — данные по странам
// Метрики: climate, air, water, longevity, radiation, altitude, latitude, stability, uv, risks
// Каждая 0–10. Веса: 0.18, 0.12, 0.10, 0.12, 0.10, 0.08, 0.08, 0.08, 0.07, 0.07
// (climate, longevity, air, water, radiation, altitude, latitude, stability, uv, risks)

window.METRICS = [
  { key: "climate",   label: "Климат",         short: "CLM", weight: 0.18, hint: "термонейтральность, амплитуда сезонов" },
  { key: "longevity", label: "Долголетие",     short: "HAL", weight: 0.12, hint: "HALE WHO 2023, годы здоровой жизни" },
  { key: "air",       label: "Воздух",         short: "AIR", weight: 0.12, hint: "PM2.5, среднегодовое, IQAir" },
  { key: "water",     label: "Вода",           short: "H2O", weight: 0.10, hint: "качество питьевой воды, WHO" },
  { key: "radiation", label: "Радиация",       short: "RAD", weight: 0.10, hint: "природный фон + радон, IAEA" },
  { key: "altitude",  label: "Высота",         short: "ALT", weight: 0.08, hint: "оптимум 0–300 м над уровнем моря" },
  { key: "latitude",  label: "Широта",         short: "LAT", weight: 0.08, hint: "оптимум 30–45°" },
  { key: "stability", label: "Стабильность",   short: "STB", weight: 0.08, hint: "отклонение от среднего, экстремумы" },
  { key: "uv",        label: "УФ-баланс",      short: "UV",  weight: 0.07, hint: "оптимум индекс 3–5 среднегод." },
  { key: "risks",     label: "Природ. риски",  short: "RSK", weight: 0.07, hint: "сейсмика, тайфуны, наводнения (inverse)" },
];

// 40 стран. Координаты — для расположения на карте (упрощ.). lat/lon реальные приближённые.
// Все метрики правдоподобные, ориентированные на оригинальный отчёт.
window.COUNTRIES = [
  { code: "PT", name: "Португалия",   region: "Юж. Европа",  lat: 39.5,  lon: -8.0,  climate: 9.5, longevity: 8.6, air: 8.8, water: 9.0, radiation: 9.0, altitude: 9.2, latitude: 9.5, stability: 9.0, uv: 9.0, risks: 8.5, anchor: "Алгарви, Лиссабон" },
  { code: "CY", name: "Кипр",         region: "Среднеземн.", lat: 35.0,  lon: 33.0,  climate: 9.4, longevity: 8.4, air: 8.5, water: 7.5, radiation: 9.2, altitude: 9.1, latitude: 9.6, stability: 8.8, uv: 8.5, risks: 8.7, anchor: "Лимассол, Пафос" },
  { code: "ES", name: "Испания",      region: "Юж. Европа",  lat: 40.0,  lon: -4.0,  climate: 9.3, longevity: 9.0, air: 8.4, water: 8.8, radiation: 8.9, altitude: 8.6, latitude: 9.4, stability: 8.9, uv: 8.8, risks: 8.6, anchor: "Малага, Балеары" },
  { code: "GR", name: "Греция",       region: "Среднеземн.", lat: 39.0,  lon: 22.0,  climate: 9.0, longevity: 8.8, air: 8.0, water: 8.4, radiation: 8.8, altitude: 8.5, latitude: 9.5, stability: 8.6, uv: 8.6, risks: 7.8, anchor: "Крит, Икария" },
  { code: "NZ", name: "Новая Зеландия", region: "Океания",   lat: -41.0, lon: 174.0, climate: 9.1, longevity: 8.9, air: 9.6, water: 9.5, radiation: 9.1, altitude: 8.7, latitude: 8.7, stability: 9.0, uv: 7.5, risks: 7.5, anchor: "Northland" },
  { code: "IT", name: "Италия",       region: "Юж. Европа",  lat: 42.0,  lon: 12.0,  climate: 8.9, longevity: 9.2, air: 7.5, water: 8.6, radiation: 8.6, altitude: 8.4, latitude: 9.3, stability: 8.4, uv: 8.7, risks: 7.8, anchor: "Сардиния, Лигурия" },
  { code: "AU", name: "Австралия",    region: "Океания",     lat: -25.0, lon: 134.0, climate: 9.0, longevity: 8.9, air: 8.9, water: 9.0, radiation: 8.5, altitude: 8.6, latitude: 9.0, stability: 8.4, uv: 6.4, risks: 7.6, anchor: "Аделаида, Перт" },
  { code: "HR", name: "Хорватия",     region: "Юж. Европа",  lat: 45.0,  lon: 16.0,  climate: 8.7, longevity: 8.4, air: 8.0, water: 8.8, radiation: 8.7, altitude: 8.4, latitude: 8.9, stability: 8.7, uv: 8.6, risks: 8.5, anchor: "Далмация, Сплит" },
  { code: "JP", name: "Япония",       region: "Вост. Азия",  lat: 36.0,  lon: 138.0, climate: 8.4, longevity: 9.8, air: 7.9, water: 9.2, radiation: 8.2, altitude: 8.6, latitude: 9.0, stability: 8.0, uv: 8.5, risks: 6.0, anchor: "Окинава, Кюсю" },
  { code: "ME", name: "Черногория",   region: "Юж. Европа",  lat: 42.7,  lon: 19.4,  climate: 8.8, longevity: 8.0, air: 8.0, water: 8.5, radiation: 8.6, altitude: 8.0, latitude: 9.0, stability: 8.6, uv: 8.6, risks: 8.6, anchor: "Будва, Бар" },
  { code: "FR", name: "Франция",      region: "Зап. Европа", lat: 46.0,  lon: 2.0,   climate: 8.4, longevity: 9.1, air: 7.8, water: 8.7, radiation: 8.5, altitude: 8.4, latitude: 8.4, stability: 8.6, uv: 8.4, risks: 8.6, anchor: "Прованс" },
  { code: "CL", name: "Чили",         region: "Юж. Америка", lat: -33.0, lon: -71.0, climate: 8.7, longevity: 8.4, air: 7.4, water: 8.0, radiation: 8.6, altitude: 8.0, latitude: 9.0, stability: 8.0, uv: 8.0, risks: 6.0, anchor: "Вальпараисо" },
  { code: "US", name: "США",          region: "Сев. Америка", lat: 32.7, lon: -117.2, climate: 8.6, longevity: 7.6, air: 8.0, water: 8.6, radiation: 8.4, altitude: 8.4, latitude: 9.0, stability: 7.8, uv: 8.2, risks: 7.4, anchor: "Сан-Диего, CA" },
  { code: "UY", name: "Уругвай",      region: "Юж. Америка", lat: -34.9, lon: -54.9, climate: 8.6, longevity: 8.2, air: 8.4, water: 8.6, radiation: 8.6, altitude: 8.6, latitude: 9.0, stability: 8.4, uv: 8.0, risks: 8.6, anchor: "Пунта-дель-Эсте" },
  { code: "TR", name: "Турция",       region: "Среднеземн.", lat: 38.4,  lon: 27.1,  climate: 8.6, longevity: 8.2, air: 7.4, water: 8.0, radiation: 8.4, altitude: 8.2, latitude: 9.4, stability: 8.0, uv: 8.4, risks: 6.6, anchor: "Измир, Чешме" },
  { code: "MT", name: "Мальта",       region: "Среднеземн.", lat: 35.9,  lon: 14.5,  climate: 8.9, longevity: 8.7, air: 7.6, water: 7.5, radiation: 8.6, altitude: 8.4, latitude: 9.5, stability: 8.7, uv: 8.4, risks: 8.7, anchor: "Валлетта" },
  { code: "IS", name: "Исландия",     region: "Сев. Европа", lat: 64.9,  lon: -19.0, climate: 6.0, longevity: 9.0, air: 9.7, water: 9.8, radiation: 8.9, altitude: 8.8, latitude: 5.5, stability: 8.0, uv: 6.0, risks: 7.0, anchor: "Рейкьявик" },
  { code: "FI", name: "Финляндия",    region: "Сев. Европа", lat: 64.0,  lon: 26.0,  climate: 5.6, longevity: 8.7, air: 9.6, water: 9.5, radiation: 8.0, altitude: 8.8, latitude: 5.0, stability: 8.5, uv: 5.5, risks: 9.2, anchor: "Хельсинки" },
  { code: "NO", name: "Норвегия",     region: "Сев. Европа", lat: 60.5,  lon: 8.5,   climate: 6.0, longevity: 9.0, air: 9.5, water: 9.7, radiation: 8.0, altitude: 8.6, latitude: 5.5, stability: 8.4, uv: 5.6, risks: 9.0, anchor: "Берген" },
  { code: "CH", name: "Швейцария",    region: "Зап. Европа", lat: 46.8,  lon: 8.2,   climate: 7.8, longevity: 9.4, air: 8.6, water: 9.4, radiation: 8.2, altitude: 7.5, latitude: 8.4, stability: 9.4, uv: 8.0, risks: 8.4, anchor: "Тичино" },
  { code: "RU", name: "Россия",       region: "Вост. Европа", lat: 55.7, lon: 37.6,  climate: 5.8, longevity: 6.4, air: 7.0, water: 7.4, radiation: 7.6, altitude: 8.4, latitude: 6.0, stability: 7.0, uv: 6.0, risks: 8.6, anchor: "Сочи (анклав 7.5)" },
  { code: "DE", name: "Германия",     region: "Зап. Европа", lat: 51.0,  lon: 10.0,  climate: 7.6, longevity: 8.7, air: 8.2, water: 9.0, radiation: 8.0, altitude: 8.5, latitude: 7.6, stability: 8.7, uv: 7.6, risks: 9.0, anchor: "Бавария" },
  { code: "GB", name: "Великобритания", region: "Зап. Европа", lat: 54.0, lon: -2.0, climate: 7.0, longevity: 8.5, air: 8.4, water: 9.0, radiation: 7.6, altitude: 8.6, latitude: 7.0, stability: 8.7, uv: 7.0, risks: 9.0, anchor: "Корнуолл" },
  { code: "CA", name: "Канада",       region: "Сев. Америка", lat: 49.3, lon: -123.1, climate: 7.4, longevity: 8.7, air: 8.8, water: 9.4, radiation: 7.8, altitude: 8.4, latitude: 7.6, stability: 8.5, uv: 7.4, risks: 8.4, anchor: "Ванкувер" },
  { code: "MX", name: "Мексика",      region: "Сев. Америка", lat: 23.6, lon: -102.5, climate: 8.5, longevity: 8.1, air: 6.8, water: 7.0, radiation: 8.2, altitude: 7.0, latitude: 8.4, stability: 7.4, uv: 7.4, risks: 7.0, anchor: "Юкатан" },
  { code: "BR", name: "Бразилия",     region: "Юж. Америка", lat: -14.2, lon: -51.9, climate: 8.0, longevity: 7.6, air: 7.5, water: 7.6, radiation: 7.8, altitude: 8.0, latitude: 7.4, stability: 7.6, uv: 6.8, risks: 7.6, anchor: "Флорианополис" },
  { code: "AR", name: "Аргентина",    region: "Юж. Америка", lat: -38.4, lon: -63.6, climate: 8.4, longevity: 7.8, air: 8.0, water: 7.8, radiation: 8.4, altitude: 8.0, latitude: 8.7, stability: 7.8, uv: 7.8, risks: 8.4, anchor: "Мар-дель-Плата" },
  { code: "CR", name: "Коста-Рика",   region: "Цент. Америка", lat: 9.7, lon: -83.7, climate: 8.6, longevity: 8.8, air: 8.0, water: 7.8, radiation: 8.6, altitude: 7.4, latitude: 7.0, stability: 8.0, uv: 6.6, risks: 7.0, anchor: "Никоя" },
  { code: "TH", name: "Таиланд",      region: "ЮВ Азия",     lat: 15.9,  lon: 100.9, climate: 7.4, longevity: 7.8, air: 6.6, water: 7.0, radiation: 8.4, altitude: 8.4, latitude: 7.4, stability: 7.6, uv: 6.0, risks: 7.6, anchor: "Чиангмай" },
  { code: "ID", name: "Индонезия",    region: "ЮВ Азия",     lat: -0.8,  lon: 113.9, climate: 7.0, longevity: 7.4, air: 6.0, water: 6.4, radiation: 8.0, altitude: 7.6, latitude: 6.6, stability: 7.0, uv: 5.6, risks: 5.4, anchor: "Бали" },
  { code: "VN", name: "Вьетнам",      region: "ЮВ Азия",     lat: 14.1,  lon: 108.3, climate: 7.4, longevity: 8.0, air: 6.5, water: 7.0, radiation: 8.2, altitude: 8.0, latitude: 7.4, stability: 7.4, uv: 6.4, risks: 6.6, anchor: "Дананг" },
  { code: "AE", name: "ОАЭ",          region: "Бл. Восток",  lat: 24.0,  lon: 53.8,  climate: 6.4, longevity: 8.4, air: 6.6, water: 8.0, radiation: 8.4, altitude: 8.7, latitude: 8.0, stability: 8.4, uv: 5.8, risks: 9.4, anchor: "Дубай" },
  { code: "ZA", name: "ЮАР",          region: "Юж. Африка",  lat: -33.9, lon: 18.4,  climate: 8.6, longevity: 7.0, air: 7.7, water: 8.0, radiation: 8.4, altitude: 8.0, latitude: 9.0, stability: 8.0, uv: 7.0, risks: 8.4, anchor: "Кейптаун" },
  { code: "MA", name: "Марокко",      region: "Сев. Африка", lat: 31.8,  lon: -7.1,  climate: 8.4, longevity: 7.8, air: 7.4, water: 7.4, radiation: 8.6, altitude: 8.0, latitude: 9.0, stability: 8.4, uv: 7.6, risks: 8.6, anchor: "Эс-Сувейра" },
  { code: "GE", name: "Грузия",       region: "Кавказ",      lat: 42.3,  lon: 43.4,  climate: 8.0, longevity: 7.8, air: 7.6, water: 8.4, radiation: 8.4, altitude: 7.6, latitude: 9.0, stability: 7.8, uv: 8.0, risks: 7.8, anchor: "Батуми" },
  { code: "AM", name: "Армения",      region: "Кавказ",      lat: 40.0,  lon: 45.0,  climate: 7.4, longevity: 7.8, air: 7.6, water: 8.4, radiation: 8.0, altitude: 6.6, latitude: 9.4, stability: 7.6, uv: 7.6, risks: 7.4, anchor: "Цахкадзор" },
  { code: "TN", name: "Тунис",        region: "Сев. Африка", lat: 33.9,  lon: 9.5,   climate: 8.5, longevity: 8.0, air: 7.6, water: 7.4, radiation: 8.6, altitude: 8.4, latitude: 9.4, stability: 8.4, uv: 7.6, risks: 8.7, anchor: "Хаммамет" },
  { code: "IL", name: "Израиль",      region: "Бл. Восток",  lat: 31.0,  lon: 35.0,  climate: 8.5, longevity: 9.2, air: 7.6, water: 8.4, radiation: 8.6, altitude: 8.4, latitude: 9.4, stability: 8.4, uv: 7.4, risks: 7.8, anchor: "Хайфа" },
  { code: "IN", name: "Индия",        region: "Юж. Азия",    lat: 20.6,  lon: 78.9,  climate: 6.6, longevity: 6.6, air: 4.2, water: 5.6, radiation: 7.4, altitude: 7.4, latitude: 8.0, stability: 6.6, uv: 5.6, risks: 6.4, anchor: "Гоа" },
  { code: "CN", name: "Китай",        region: "Вост. Азия",  lat: 35.0,  lon: 105.0, climate: 7.4, longevity: 8.4, air: 5.6, water: 6.6, radiation: 7.6, altitude: 7.0, latitude: 8.4, stability: 7.2, uv: 6.8, risks: 6.4, anchor: "Хайнань" },
];

// Подсчёт BOI с пользовательскими весами
window.computeBOI = function (country, weights) {
  let sum = 0, wsum = 0;
  for (const m of window.METRICS) {
    const w = weights[m.key] ?? m.weight;
    sum += (country[m.key] ?? 0) * w;
    wsum += w;
  }
  return wsum > 0 ? sum / wsum : 0;
};
