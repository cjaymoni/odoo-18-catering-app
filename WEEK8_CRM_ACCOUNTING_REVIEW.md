# Review 4 – End of Week 8: CRM & Accounting Review

Goals

- Confirm VAT setup, chart of accounts, tax configuration for Ghana
- Review invoice generation, journal entry logic, and tax computations
- Validate multicurrency handling (rates, GHS vs USD/GBP workflows)
- Ensure CRM pipeline stages reflect customer lifecycle
- Review linkages between leads, requests, and bookings

---

## Summary

The core catering flows are in place (booking, SO creation, WhatsApp, UI). Accounting and CRM integration exist at a basic level but need setup and a few enhancements to meet the goals above. Key items: use Odoo’s tax engine instead of a hard‑coded VAT, wire standard invoicing into the booking flow, configure multicurrency properly, and connect CRM opportunities to bookings with lifecycle stage sync.

## 1) VAT, Chart of Accounts, Ghana Tax Configuration

Findings

- No dependency on a Ghana localization; chart of accounts not enforced by the module.
- Booking totals compute VAT with a fixed 15% multiplier in `cater.event.booking` (not via `account.tax`).
- Products created on the fly for SO lines do not assign any tax, so invoices won’t carry configured taxes automatically.

Recommendations

- Install a Ghana localization and chart of accounts:
  - Apps → install `l10n_gh` (if not available, pick the most appropriate localization or configure a standard CoA).
  - In Accounting → Configuration → Chart of Accounts, apply the Ghana template to the company.
- Create or verify a 15% VAT Sales tax (`account.tax`) applicable on sales.
- Set company default sales taxes and/or product taxes to this VAT where applicable.
- Refactor booking totals to rely on product taxes on SO/invoices rather than a hard-coded 15% in the booking model. Keep booking totals as indicative UI numbers, or compute from SO lines.
- Ensure newly created products in `_get_or_create_product()` get the default sales tax if set (leave detailed tax logic to Accounting configuration).

Validation

- Create a test booking → Confirm → Generate SO → Create/Confirm Invoice. The invoice lines must show the 15% VAT tax; journal entries should include tax accounts defined by the CoA.

## 2) Invoice Generation & Journal Entries

Findings

- On confirm, the booking creates a `sale.order` only; no invoice is created automatically.
- `account.move` is extended to reference the booking (`catering_booking_id`) for traceability, but no creation logic is provided.

Recommendations

- Provide a button on the booking to create an invoice from the related Sales Order (or rely on standard SO flow: Confirm SO → Create Invoice).
- When creating invoices, set `catering_booking_id` on the invoice for linkage (this is already supported by the model extension).
- Let Odoo’s accounting generate the journal entries; verify taxes and accounts via CoA configuration.

Validation

- Confirm a booking, open the SO, click Create Invoice (down payment or regular). Post the invoice and confirm journal entries include VAT accounts.

## 3) Multicurrency Handling (GHS vs USD/GBP)

Findings

- `currency_id` exists on bookings and lines, defaulting to the company currency. Computations occur directly in that currency; no on-the-fly conversion is implemented.
- No explicit exchange rate configuration in the module; relies on Odoo standard.

Recommendations

- Company currency: set to GHS if operating locally.
- Enable currency rates: Accounting → Configuration → Currencies → activate USD, GBP; enable an exchange rate provider with daily rates.
- For international quotes:
  - Use pricelists and select the target currency on the Sales Order.
  - Ensure the invoice uses the SO currency; Odoo will handle conversion in reporting and journal entries.
- Optional: Allow selecting a currency at booking level and propagate to the SO; keep booking display amounts in that currency for consistency.

Validation

- Create a USD quote: set SO currency to USD; verify invoice amounts and company currency reporting/entries reflect exchange rates.

## 4) CRM Pipeline Stages & Lifecycle

Findings

- The module depends on `crm` but does not define custom stages or link stages to booking states.
- No explicit relationship field to `crm.lead` on bookings.

Recommendations

- Define lifecycle mapping:
  - CRM: New → Qualified → Quote Sent → Negotiation → Won/Lost
  - Booking: Draft → Confirmed → In Progress → Completed/Cancelled
- Link events:
  - When a booking creates a Sales Order, move the related lead to “Quote Sent”.
  - When booking is confirmed, mark the opportunity as “Won”. On cancellation, set to “Lost”.
- Add fields/links:
  - `cater.event.booking.lead_id` (Many2one to `crm.lead`)
  - Smart buttons: from lead, see related bookings; from booking, open the lead/opportunity.
  - Optionally a “Create Booking from Opportunity” action in CRM.

Validation

- Create lead → create booking from it → confirm booking → verify opportunity moves to Won. Cancellations should mark it Lost.

## 5) Linkages: Leads, Requests, and Bookings

Findings

- No explicit linkage today other than the shared partner.

Recommendations

- Introduce explicit lead-to-booking linkage as above.
- If you collect “requests” (e.g., portal request forms) separate from CRM leads, normalize them by creating a lead record first, then converting to a booking.
- Add chatter messages on both records when state transitions occur for traceability.

Validation

- From a portal/customer request, ensure a lead is generated; upon qualification, convert to a booking and keep cross-links.

## Action Plan (Next Sprint)

- Accounting
  - Install/verify `l10n_gh` and Ghana CoA; set 15% VAT Sales tax and default taxes.
  - Update product creation to inherit default taxes; remove hard-coded VAT from booking totals or mark as indicative only.
  - Add a booking button to create invoice from SO and set `catering_booking_id` on invoices.
- Multicurrency
  - Enable rates provider; verify USD/GBP flows via SO/pricelists; propagate booking currency to SO.
- CRM
  - Add `lead_id` on booking; smart buttons and actions to create booking from opportunity.
  - Implement stage sync (SO creation → Quote Sent; booking confirm → Won; cancel → Lost).
- QA/Docs
  - Add tests: VAT on invoice lines, multicurrency USD quote, CRM stage transitions.
  - Extend README with Ghana accounting setup steps and multicurrency notes (link here).

## Quick Checks & How-To

- Ghana CoA and VAT: Accounting → Configuration → Taxes/Chart of Accounts
- Default taxes: Accounting → Configuration → Settings → Taxes
- Currency rates: Accounting → Configuration → Currencies → Providers
- CRM stages: CRM → Configuration → Pipeline Stages
- Lead/Booking link: once implemented, use smart buttons on both records

---

Status: Recommendations prepared. No breaking changes were introduced. Proceed with configuration and incremental enhancements above.
