# Use Case Diagram — Mandi 1 Restaurant Website

```mermaid
graph TB
    Customer((Customer))
    Admin((Admin / Staff))

    subgraph "Mandi 1 System"
        UC1[Browse Menu & Deals]
        UC2[Add Items to Cart]
        UC3[Update / Remove Cart Items]
        UC4[Enter Contact Details]
        UC5[Confirm Order - Pay on Pickup]
        UC6[Chat with AI Assistant]
        UC7[Receive Order & Contact Details]
        UC8[Call Customer to Confirm Order]
        UC9[Update Order Status]
        UC10[Add / Edit / Delete Dishes]
        UC11[Manage Categories]
        UC12[Create Discounts & Deals]
        UC13[Adjust Price & Stock Quantity]
        UC14[View Dashboard Statistics]
        UC15[Staff Login / Logout]
    end

    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    Customer --> UC6
    UC5 -.includes.-> UC4

    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    Admin --> UC13
    Admin --> UC14
    Admin --> UC15
    UC9 -.includes.-> UC8
```

**Actors**
- **Customer** — any site visitor placing a takeaway order.
- **Admin / Staff** — restaurant staff who manage the menu and confirm orders by phone.

**Key flow:** Customer browses → adds to cart → confirms order (provides name, phone, email) →
Admin receives the order in the staff dashboard → Admin calls the customer to confirm →
Admin updates the order status (Confirmed → Completed).
