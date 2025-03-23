import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import HttpApi from "i18next-http-backend";
import LanguageDetector from "i18next-browser-languagedetector";

import enTranslation from "./en/translation.json";
import huTranslation from "./hu/translation.json";
import roTranslation from "./ro/translation.json";

i18next
  .use(HttpApi)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    returnNull: false,
    resources: {
      en: { translation: enTranslation },
      hu: { translation: huTranslation },
      ro: { translation: roTranslation }
    }
  });

export default i18next;
