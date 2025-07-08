# Julep_ai

## Project Overview
Julep_ai is a Flask-based web application that provides AI-powered food recommendations based on user preferences and city data. It integrates with APIs and models such as Julep, DeepSeek, and Llama to deliver personalized suggestions. The app features a modular codebase, a simple UI, and uses environment variables for configuration.

## AI Models Used

### Llama
- **Why:**  
  Llama is a state-of-the-art large language model used in this project for understanding user queries, generating natural language responses, and providing context-aware recommendations.
- **How:**  
  When a user interacts with the app, Llama helps interpret their intent and refines the recommendation process, making suggestions more relevant and conversational.

### DeepSeek
- **Why:**  
  DeepSeek is used for extracting structured information (like city names) from user input.
- **How:**  
  When a user mentions a city or location, DeepSeek accurately identifies and extracts this information, ensuring that recommendations are specific to the user’s intended location.

## Major Features
- Flask web server with static and template directories
- Integration with Julep API and other AI models
- Modular code for user, city, and recommendation handling
- Environment variable support for API keys and configuration
- Basic UI for adding cities and viewing recommendations

## Missing Features / Areas for Improvement
- **Sensitive Data Security:** `.env` was previously committed, exposing API keys. Keys should be rotated and `.env` must be in `.gitignore`.
- **User Authentication:** No login or user management yet.
- **Database Integration:** Data is stored in JSON files, not a scalable database.
- **Error Handling:** Limited input validation and error management.
- **Automated Testing:** No unit or integration tests.
- **Deployment:** No Dockerfile or deployment instructions.

## Unique Feature: Personalized Recommendation History

**Description:**  
Users can log in and view a history of all their past food recommendations, including the cities and restaurants suggested. They can also rate previous recommendations, helping the system improve future suggestions.

**How to Use:**
1. Register or log in to your account.
2. Use the app to get food recommendations as usual.
3. Click on the "My History" link in the navigation bar to view your past recommendations and provide feedback.

**How It Works:**
- Each time you receive a recommendation, it is saved to your personal history.
- You can revisit and rate previous recommendations, making your experience more personalized.

**Planned Implementation:**
- Add user authentication with Flask-Login.
- Store recommendation history in a database (e.g., SQLite).
- Create a `/history` route and template to display the user's history.
- Allow users to rate and comment on past recommendations.

*This feature will make the app more engaging and tailored to each user!*
