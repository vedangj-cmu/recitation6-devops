# E-commerce Azure Functions: Warehouse, Cart, Inventory & Checkout

This project contains the backend logic for an e-commerce application, built as a set of serverless Azure Functions. It includes functions for managing:

*   **Warehouse**: Handles stock levels and logistics.
*   **Inventory**: Provides real-time product availability.
*   **Cart**: Manages user shopping carts.
*   **Checkout**: Processes orders and payments.

This guide provides the quickest way to deploy these functions to Azure using Visual Studio Code.

## Step 1: Install the Azure Functions Extension

Before you begin, you need the official Azure Functions extension for Visual Studio Code.

1.  Open Visual Studio Code.
2.  Go to the **Extensions** view (or press `Ctrl+Shift+X`).
3.  Search for `Azure Functions`.
4.  Find the extension published by Microsoft and click **Install**.

## Step 2: Get the Project Code

You have two options:

*   **Use this Project**: If you have cloned this repository, simply open the project folder in Visual Studio Code.
*   **Create a New Project**: You can also create a new Azure Functions project from scratch using the VS Code extension and then copy the function code from this repository into it.

## Step 3: Deploy to Azure

With the project open in VS Code, you can deploy it in just a few clicks.

1.  **Sign in to Azure**: Open the **Azure** view from the Activity Bar. If you aren't signed in, you will be prompted to do so.
2.  **Click Deploy**: In the **Workspace** section of the Azure view, find the "Deploy..." button (a blue up-arrow icon) and click it.
3.  **Follow the Prompts**:
    *   Choose **"Deploy to Function App..."**.
    *   Select your Azure Subscription.
    *   Choose **"Create new Function App in Azure..."** and follow the on-screen instructions to name your app, select a runtime, and choose a region.

The extension will handle the rest. Once the process is complete, your e-commerce functions will be live on Azure!

### Redeploying Changes

If you make any changes to your code, simply click the **Deploy** button again. The extension will create a new zip file with your updated code and redeploy it to the same Function App, overwriting the previous version.

## Step 4: Expose Functions via API Management (Optional)

Once your functions are deployed, you can use Azure API Management to create a professional, secure, and scalable API gateway for them. This allows you to manage access, apply policies (like rate limiting or authentication), and provide a unified API endpoint for your consumers.

1.  **Navigate to your Function App**: Open the [Azure Portal](https://portal.azure.com) and go to the Function App you just deployed.
2.  **Find API Management**: In the left-hand navigation menu of your Function App, scroll down to the "API" section and click on **API Management**.
3.  **Create or Link an Instance**:
    *   You will be prompted to link to an existing API Management instance or create a new one.
    *   Follow the on-screen instructions to configure your API Management service.
4.  **Import Functions**: During the process, you can select which of your HTTP-triggered functions you want to import as APIs into your API Management instance.

After the process completes, your functions will be accessible through the API Management gateway endpoint, giving you a powerful layer of control and abstraction.


## Database Connection

All functions in this project share a common module for database connectivity located in `db.py`. This module uses the `pyodbc` library to connect to an Azure SQL Database.

The connection string is retrieved from an environment variable within the code:
```python
os.environ["SQLCONNSTR_SQL_CONN_STR"]
```

### The `SQLCONNSTR_` Prefix

The `SQLCONNSTR_` prefix is a special convention used by Azure Functions. When the function host sees this prefix, it tells the function to look for a setting named `SQL_CONN_STR` in the **Connection Strings** section of your Function App's configuration on the Azure Portal.

This is the recommended practice as it allows you to securely store your database credentials separately from your application code and manage them as typed connection strings within Azure.