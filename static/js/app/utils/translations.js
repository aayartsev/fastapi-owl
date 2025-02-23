const translations = {
    ru: {
      hello: "Привет",
      yes: "Да",
      no: "Нет",
    },
  };
export  const translateFn = (str, ctx) => translations[ctx]?.[str] || str;
