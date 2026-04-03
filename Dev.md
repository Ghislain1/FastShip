# GrundIdee
- Product → Produkte (z. B. Ball, Schuhe)
- Seller → Verkäufer (wer verkauft das Produkt)
- Order → Bestellung (Kunde kauft etwas)
- Shipment → Lieferung (wie die Bestellung verschickt wird)
- Beziehungen
  -   Seller → Product  (One-to-Many)
  -   Order → Product (Many-to-Many)
  -   Order → Shipment (1 : 1 oder 1 : N) = Eine Bestellung hat eine oder mehrere Lieferungen
- Shipment Status
  - pending → Bestellung eingegangen, noch nicht versendet
  - processing → wird vorbereitet/verpackt
  - shipped → wurde verschickt
  -  in_transit → unterwegs
  -  out_for_delivery → in Zustellung
  -  delivered → zugestellt ✅
  -  failed → Zustellung fehlgeschlagen ❌
  -  returned → zurückgeschickt
- Shipment Table Model
  - id → eindeutige ID der Lieferung
  - order_id → zu welcher Bestellung die Lieferung gehört
  - status → aktueller Status (z. B. „shipped“, „delivered“)
  - tracking_number → Sendungsnummer
  - carrier → Versanddienst (z. B. DHL)
  - shipped_date → wann verschickt
  - delivery_date → wann zugestellt
  - estimated_delivery → erwartetes Lieferdatum
- Order:
  - id (PK)
  - customer_id  → welcher Kunde bestellt hat
  - order_date
  - status
  - total_amount
  - currency
  - payment_method
  - payment_status  → bezahlt / offen
  - billing_address_id
  - shipping_address_id
  - created_at
  - updated_at

- Product:
  - id (PK)
  - seller_id (FK → Seller.id)
  - name
  - description
  - price
  - currency
  - stock_quantity
  - category
  - sku
  - weight
  - created_at
  - updated_at
  
- Seller:
  - id (PK)
  - name
  - email
  - phone
  - company_name
  - tax_id
  - address_id
  - rating
  - created_at
  - updated_at

# Scalar Fast API
- package scalar-fastapi
- Scalar API Reference Plugin for FastAPI
- https://scalar.com/products/api-references/integrations/fastapi
## Register User (Section 11)
- Seller Model
  - Represent a table  Seller
  - Customer
- Signup Endpoint
  - To register a Seller or Customer
  - Custom password to be hashed
-  Password Hash
   -  Hashing Algo
   -  understand package passlib[bcrypt]
- Seller Login
  - PassWordRequestForm class
  - Usage JWT Token
  - 


# Tasks
- https://www.youtube.com/watch?v=SR5NYCdzKkc&t=6351s
     - Database Connection
- Pizza Delivery API
-  https://www.youtube.com/watch?v=mPHZKqUgnDU&list=PLEt8Tae2spYnLMAf8RGCNYhovIFZHVsPP&index=3
-  

