
# Fcommerce: Empowering Businesses Online  

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Live Demo and Documentation](#live-demo-and-documentation)
- [Installation](#installation)
- [Usage](#usage)
    - [With Facebook Page](#with-facebook-page)
    - [Without Facebook Page](#without-facebook-page)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)


## Overview

Fcommerce is a versatile Django-based web application designed to empower businesses, whether they have a Facebook page or not, to create and manage their own websites outside of Facebook. Fcommerce seamlessly integrates with Facebook's product catalog, keeping inventory synchronized, and offers an integrated sandbox payment gateway for secure transactions.  


## Features  

- **Facebook Page Integration (Optional)**: Fcommerce provides the option to link your existing Facebook page. This allows automatic product synchronization with your Facebook product catalog. For businesses without a Facebook page, Fcommerce can be used as a standalone website management system.

- **Product Management**: Include Necessery feature for product and inventory management.

- **Product Catalog Sync**: Fcommerce ensures real-time synchronization of your product data with the Facebook product catalog. Any changes you make on your website are automatically reflected in your Facebook catalog, maintaining an up-to-date inventory.  

- **Payment Gateway Integration**: I integrated sandbox payment gateway that handles checkouts and payments securely, offering a seamless shopping experience for your customers.  


## Live Demo and Documentation

* [Live Demo](https://fcommerce.monirhossain.dev)
* [Swagger API Documentation](https://fcommerce.monirhossain.dev/schema/swagger)
* [Redoc API Documentation](https://fcommerce.monirhossain.dev/schema/redoc)


## Installation

Getting started with Fcommerce is easy:

1. Clone this repository to your local machine

   ```bash
   git clone git@github.com:pi3o1416/Fcommerce.git
   cd Fcommerce

2. Create a virtual environment and activate it.

    ```bash
    virtualenv -p /usr/bin/python3.9 venv   # This is developed and tested in python 3.9 however you can try other python version
    source venv/bin/activate
    
3. Install required dependencies.

    ```bash
    pip install -r requirements.txt

4. Configure Project environment (I strongly recommend running this on development mode)
5. Run Database Migrations
    ```bash
    python manage.py migrate
6. Start Development Server
    ```bash
    python manage.py runserver
    
## Usage

### With Facebook Page
1. Link your Facebook page to Fcommerce to start automatic product synchronization.
2. Manage your product catalog within Fcommerce.
3. Customers can visit your website, browse products, and complete purchases securely using the integrated sandbox payment gateway.

### Without Facebook Page
1. Use Fcommerce as a standalone website management system.
2. Manage your product catalog, customize your website, and handle payments independently.


## Contributing


Contributions to Fcommerce are welcome! If you have suggestions, encounter issues, or want to contribute to our open-source project, please open a GitHub issue or submit a pull request.

## License


This project is licensed under the MIT License. See the [LICENSE](https://github.com/pi3o1416/Fcommerce/blob/development/LICENSE) file for details.

## Acknowledgments


*   [Django](https://www.djangoproject.com/)
*   [Facebook Graph API](https://developers.facebook.com/docs/graph-api/)
*   [aamarpay Payment Gateway](https://aamarpay.com/)

* * *

