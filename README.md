# Recipta

This is a project for processing shopping products from receipts, APIs, or manual input to keep track of prices and help estimate cart price.

### Features currently under development

- Receipt reading

  - Image should be cropped and cleaned from noise
  - OCR text is forwarded to LLM
  - LLM prompt is engineered to make the LLM return a structured output

- Saving & retreiving user data:
  - User auth
  - Scans
  - Products: CRUD operations on purchased products
  - Query the products

### Future features:

- Shops / locations

  - Add shop details (e.g. address, API site, etc)
  - Create a trip optimizer for visiting multiple locations (might just use Google maps API on client side app)
  - Track and view price trends with charts and account for discounts & predict prices (linear regression)

- Tags
  - Create tags for different categories and product names
  - Tag products with relevant tags for easier searching
