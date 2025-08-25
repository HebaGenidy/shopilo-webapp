# E-Commerce Web App


## Project Aim
Create a simple web platform for online shopping with basic CRUD operations.

## Required pages
**All Pages should have the same NavBar**
1. Home page
2. All Products page
3. Product details page
4. All Categories page
5. Category page that contains all products that belongs to it
6. Registration page
7. Login page
8. User Profile page

## Features

### 1. Homepage

The homepage should contain the following:
- **All products** (ordered by recently added)
- **Categories list**
- **Search bar** for products (Bonus)

### 2. Navigation Bar

The website should have a **navigation bar** present on all pages containing:
- **Home** link (to homepage)
- **All Products** link (to view all products)
- **Categories** link (to view all categories)
- **Login/Logout** links (depending on user authentication status)
- **Profile** link (visible for authenticated users only)
- **Admin Panel** link (visible for admin users only) (Bonus)

### 3. Products

#### Product Management (Admin)
The admin can manage products which includes:
- **Add new product** with:
  - Product name
  - Description
  - Price
  - Category (from predefined categories)
  - Product image
  - Stock count
- **Edit existing products**
- **Delete products**
- **View all products**


#### Product Browsing (Users)
- Users can view all products
- Users can view product details
- Users can search products by name (Bonus)
- Users can filter products by category (Bonus)

### 4. Categories

#### Category Management (Admin)
- **Add new categories**
- **Edit existing categories**
- **Delete categories**
- **View all categories**
- Admin can add categories to be used when creating products
- Each product belongs to one category (One-to-Many relationship)
- Categories must be created before products can be assigned to them

#### Category Browsing (Users)
- Users can view all categories
- Users can click on a category to view its products

### 5. Authentication System

#### **Unauthenticated users can only view home page**
- **Registration**
  - Users can register with:
    - **Username** (Unique, no users can have the same username)
    - **First name**
    - **Last name**
    - **Email** (Unique, no users can have the same email)
    - **Password**
    - **Confirm password**
    - **Profile Picture**


#### Login
- The user should be able to login after registration using username and password

#### Logout
- The user should be able to logout

#### User Profile
The user can view his profile which includes:
- View his profile
- Edit all his data except for the username & email (Bonus)

#### Account Management
- User can delete his account 

## User Roles

### Regular User
- Browse products and categories
- Manage his profile

### Admin User
- All regular user permissions
- Add/Edit/Delete products
- Add/Edit/Delete categories



## Important Note
⚠️ **Focus on implementing basic CRUD operations first before adding advanced features**
⚠️ **Search for the is_staff attribute in authentication**
⚠️ **Search for how to implement search and filteration in django (Bonus)**
