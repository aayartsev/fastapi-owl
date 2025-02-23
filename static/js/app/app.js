import { mount, whenReady } from "@odoo/owl";
import { translateFn } from "@utils/translations"
import { TEMPLATES } from "@utils/templates_loader"
import { WebClient } from "@webclient/web_client"


const env = {
  _t: translateFn,
  templates: TEMPLATES,
  dev: true,
  name: "OXP Demo App"
};

// Mount the Page component when the document.body is ready
whenReady(() => {
  mount(WebClient, document.body, env);
});