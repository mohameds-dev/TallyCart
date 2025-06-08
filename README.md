# Recipta

This is a project for processing shopping items from receipts, APIs, or manual input to keep track of prices and help estimate cart price.

### Features currently under development

- Receipt reading
    - Image should be cropped and cleaned from noise
    - OCR text is forwarded to LLM
    - LLM prompt is engineered to make the LLM return a structured output

- Saving & retreiving user data:
    - User auth
    - Scans
    - Items: CRUD operations on purchased items
    - Query the items


### Future features:

- Shops / locations
    - Add shop details (e.g. address, API site, etc)
    - Create a trip optimizer for visiting multiple locations (might just use Google maps API on client side app)
    - Track and view price trends with charts and account for discounts & predict prices (linear regression)

- Tags
    - Create tags for different categories and item names
    - Tag items with relevant tags for easier searching
