import { loadFile } from "@odoo/owl";

const asstetsJsonString  = await loadFile("/static/js/app/utils/xml_assets.json");
const assetsData = JSON.parse(asstetsJsonString)

export const TEMPLATES = new DOMParser().parseFromString("<odoo/>", "text/xml");

function loadXmlTemplate(xml){
    const doc = new DOMParser().parseFromString(xml, "text/xml");
    if (doc.querySelector("parsererror")) {
        // The generated error XML is non-standard so we log the full content to
        // ensure that the relevant info is actually logged.
        throw new Error(doc.querySelector("parsererror").textContent.trim());
    }

    for (const element of doc.querySelectorAll("templates > [t-name]")) {
        element.removeAttribute("owl");
        const name = element.getAttribute("t-name");
        const previous = TEMPLATES.querySelector(`[t-name="${name}"]`);
        if (previous) {
            console.debug("Override template: " + name);
            previous.replaceWith(element);
        } else {
            TEMPLATES.documentElement.appendChild(element);
        }
    }
}
    
const collectAllTemplates = async () => {
    await Promise.all(
        assetsData.map(async (xmlTeplateFile) => {
            const xmlFileContent = await loadFile(xmlTeplateFile);
            loadXmlTemplate(xmlFileContent)
        })
    );
};

await collectAllTemplates()