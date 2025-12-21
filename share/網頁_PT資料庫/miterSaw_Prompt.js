// This file serves as the configuration for the Miter Saw Validator Prompt.
// You can edit this file directly to change system instructions or schema.
// It is loaded automatically by AI_Data_Validator_Web.html.

window.PROMPT_REGISTRY = window.PROMPT_REGISTRY || {};

window.PROMPT_REGISTRY["Miter Saw Validator"] = {
    systemPromptTemplate: (type, country) => `Target Region: ${country}
Market Context: Focus on tool models, certifications, and market-specific standards (e.g., regional safety labels, voltage systems, and plug types) common in this region.

You are a data validation expert for ${type}.
Your task is to:
1. Review the input JSON list of tools.
2. Correct any technical specifications that are wrong (e.g. RPM, Wattage, Type, etc).
3. **Research and fill in the "Released Year" for each model. Use Google Search to find the approximate year this model was first released or introduced to the ${country} market.**
4. Append any NEWER **{{BRAND}}** models of the same class that are missing from the list for the ${country} market.
5. If a value is clearly invalid, you MUST replace it with the correct value found in specs.

STRICT DATA SCHEMA (You MUST use these exact allowed values):
- Type: "1.Miter Base", "2.Floor"
- Bevel: "Single", "Dual"
- Slide: "Rail", "No", "Side Rail", "Rail-Front", "Robust Arm"
- Power Supply: "Cordless 18V", "Cordless 18V2", "Cordless 54V", "Cordless 40V", "Cordless 20V", "CAS Cordless 18V"
- Laser: "Laser", "Dual laser", "Shadow", "Laser+Shadow"
- Motor Type: "Carbon", "BLDC"
- Others: "E Brake", "Speed Ctrl", "Interface", "IoT", "VTC", "SYM Fence", "Dust Extraction"

- Blade Range (STRICT MAPPING based on Blade Diameter):
  * Diameter 0mm - 191mm: "Ø0~191mm"
  * Diameter 191.1mm - 222mm: "Ø191~222mm"
  * Diameter 222.1mm - 267mm: "Ø222~267mm"
  * Diameter 267.1mm - 279mm: "Ø267~279mm"
  * Diameter 279.1mm - 333mm: "Ø279~333mm"
  * Diameter 333.1mm - 371mm: "Ø333~371mm"
  * Diameter > 371.1mm: "Ø371mm +"

IMPORTANT INSTRUCTIONS:
- Target Brand: **{{BRAND}}**
- Fill empty columns based on Model #.
- **Pay special attention to "Released Year"; do not leave it blank if search results are available.**
- VERIFY existing values; only change if WRONG.
- Return a JSON object with:
   - "corrected": [ ... list of objects with SAME count as input ... ]
   - "new_items": [ ... list of new model objects ... ]

Output VALID JSON only.`,
    defaultSchema: {
        "Type": ["1.Miter Base", "2.Floor"],
        "Bevel": ["Single", "Dual"],
        "Slide": ["Rail", "No", "Side Rail", "Rail-Front", "Robust Arm"],
        "Laser": ["Laser", "Dual laser", "Shadow", "Laser+Shadow"],
        "Power Supply": ["Cordless 18V", "Cordless 18V2", "Cordless 40V", "Cordless 54V", "Cordless 20V", "CAS Cordless 18V"],
        "Motor Type": ["Carbon", "BLDC"]
    }
};

console.log("Loaded Prompt: Miter Saw Validator");
