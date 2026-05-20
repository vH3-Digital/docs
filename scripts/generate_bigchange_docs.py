#!/usr/bin/env python3
"""Generate BigChange API reference MDX — one curl per endpoint."""

from __future__ import annotations

import json
from pathlib import Path

BASE = "https://api.vh3connect.io/api:YdihQNr3"
HDR = "X-API-Key: your-api-key"
OUT = Path(__file__).resolve().parent.parent / "api-reference" / "bigchange"


def curl_get(path: str, query: list[tuple[str, str]] | None = None) -> str:
    lines = [f'curl -G "{BASE}{path}" \\', f'  -H "{HDR}" \\']
    for k, v in (query or []):
        lines.append(f'  --data-urlencode "{k}={v}" \\')
    lines[-1] = lines[-1].rstrip(" \\")
    return "\n".join(lines)


def curl_post(path: str, body: dict | None = None) -> str:
    b = json.dumps(body or {"pageNumber": 1, "pageSize": 20}, indent=2)
    return (
        f'curl -X POST "{BASE}{path}" \\\n'
        f'  -H "{HDR}" \\\n'
        f'  -H "Content-Type: application/json" \\\n'
        f"  -d '{b}'"
    )


def E(method: str, path: str, desc: str, *, query=None, body=None, enums=None):
    return dict(method=method, path=path, desc=desc, query=query, body=body, enums=enums)


def block(e: dict) -> str:
    m, p, d = e["method"], e["path"], e["desc"]
    lines = [f"### `{m}` `{p}`", "", d, ""]
    if e.get("enums"):
        lines += ["**Enum values:**", ""]
        for k, vals in e["enums"].items():
            lines.append(f"- **{k}:** {', '.join(f'`{v}`' for v in vals)}")
        lines.append("")
    lines += ["```bash", curl_get(p, e.get("query")) if m == "GET" else curl_post(p, e.get("body")), "```", ""]
    return "\n".join(lines)


def page(title: str, desc: str, sections: list, extra: str = "") -> str:
    parts = [
        "---", f"title: {title}", f"description: {desc}", "---", "",
        f"# {title}", "", f"{desc}. Auth: `X-API-Key` header. Base: `{BASE}`.",
        "", extra.strip(), "",
    ]
    if extra:
        parts.append("")
    for h, intro, eps in sections:
        parts += [f"## {h}", "", intro, ""]
        for e in eps:
            parts.append(block(e))
    return "\n".join(parts).rstrip() + "\n"


COMMON = """
## Shared parameters

| Param | Type | Description |
|-------|------|-------------|
| `pageNumber` | integer | Page index (1-based) |
| `pageSize` | integer | Items per page (default 100, max 1000) |
| `sortBy` | string | Sort field (endpoint-specific) |
| `direction` | enum | `ascending` or `descending` |

## Date ranges

Where `createdAtFrom` / `createdAtTo` (or `dueDateFrom` / `dueDateTo`) apply, the span **must not exceed 12 months**. Format: ISO 8601 UTC. See [overview](/api-reference/bigchange/overview#date-ranges).
"""

PAGES = {
    "contacts": page(
        "Contacts", "BigChange contacts, groups, and site access hours",
        [
            ("Contacts", "Customer and site records.", [
                E("GET", "/contacts/contact", "Get contact.", query=[("contactId", "12345")]),
                E("POST", "/contacts/create", "Create contact.", body={"name": "Acme", "reference": "ACME-01"}),
                E("POST", "/contacts/edit", "Update contact.", body={"contactId": 12345, "name": "Acme Ltd"}),
                E("POST", "/contacts/list", "List contacts.", body={"pageNumber": 1, "pageSize": 50, "sortBy": "name", "direction": "ascending"}),
                E("POST", "/contacts/on_stop", "Put on stop.", body={"contactId": 12345, "status": "contactOnStop", "stopReason": "Credit hold"},
                  enums={"status": ["contactOnStop", "creditLimitOnStop"]}),
                E("POST", "/contacts/unstop", "Remove stop.", body={"contactId": 12345, "appliesTo": "contactOnly"},
                  enums={"appliesTo": ["contactOnly", "contactAndChildren"]}),
                E("POST", "/contacts/site_access_hours_list", "List access hours.", body={"contactId": 12345, "pageNumber": 1, "pageSize": 10}),
                E("POST", "/contacts/site_access_hours_update", "Update access hours.", body={"contactId": 12345, "body": [{"dayOfWeek": "monday", "startTime": "08:00", "endTime": "17:00"}]}),
            ]),
            ("Contact groups", "Organise contacts.", [
                E("GET", "/contact_groups/contact_group", "Get group.", query=[("contactGroupId", "99")]),
                E("POST", "/contact_groups/create", "Create group.", body={"name": "Retail"}),
                E("POST", "/contact_groups/list", "List groups.", body={"pageNumber": 1, "pageSize": 50}),
                E("POST", "/contact_groups/update", "Update group.", body={"contactGroupId": 99, "name": "Retail UK"}),
            ]),
        ],
    ),
    "jobs": page(
        "Jobs", "BigChange jobs, constraints, stock, groups, and types",
        [
            ("Jobs", "Job lifecycle.", [
                E("GET", "/jobs/job", "Get job.", query=[("jobId", "12345")]),
                E("POST", "/jobs/create", "Create job.", body={"typeId": 42, "contactId": 12345, "description": "Blocked toilet"}),
                E("POST", "/jobs/edit", "Update job.", body={"jobId": 12345, "description": "Updated description"}),
                E("POST", "/jobs/list", "List jobs.", body={"pageNumber": 1, "pageSize": 20, "createdAtFrom": "2026-01-01T00:00:00Z", "createdAtTo": "2026-12-31T23:59:59Z", "direction": "descending"}),
                E("POST", "/jobs/cancel", "Cancel job.", body={"jobId": 12345, "reason": "Customer cancelled"}),
                E("POST", "/jobs/start", "Start job.", body={"jobId": 12345, "comment": "On site"}),
                E("POST", "/jobs/result", "Set result.", body={"jobId": 12345, "status": "completedOk", "result": "Job complete"},
                  enums={"status": ["completedOk", "completedWithIssues"]}),
                E("POST", "/jobs/scheduling", "Schedule job.", body={"jobId": 12345, "resourceId": 100, "vehicleId": 50, "plannedStartAt": "2026-04-20T09:00:00Z"}),
                E("POST", "/jobs/status/history", "Status history.", body={"jobId": 12345, "pageNumber": 1, "pageSize": 50}),
            ]),
            ("Job constraints", "Scheduling constraints.", [
                E("POST", "/jobs/constraints/create", "Create constraint.", body={"jobId": 12345}),
                E("POST", "/jobs/constraints/delete", "Delete constraint.", body={"jobId": 12345, "constraintId": 1}),
                E("POST", "/jobs/constraints/list", "List constraints.", body={"jobId": 12345, "pageNumber": 1, "pageSize": 20}),
            ]),
            ("Job stock", "Parts on jobs.", [
                E("POST", "/jobs/stock/create", "Add stock line.", body={"jobId": 12345, "stockDetailsId": 10, "quantityPlanned": 1}),
                E("POST", "/jobs/stock/delete", "Remove stock line.", body={"jobId": 12345, "jobStockId": 5}),
                E("POST", "/jobs/stock/get", "Get stock line.", body={"jobId": 12345, "jobStockId": 5}),
                E("POST", "/jobs/stock/list", "List stock lines.", body={"jobId": 12345, "pageNumber": 1, "pageSize": 20}),
            ]),
            ("Job groups", "Multi-job programmes.", [
                E("POST", "/job_groups/create", "Create group.", body={"name": "Refurb phase 1"}),
                E("POST", "/job_groups/edit", "Update group.", body={"jobGroupId": 10, "name": "Refurb phase 1"}),
                E("POST", "/job_groups/job_group", "Get group.", body={"jobGroupId": 10}),
                E("POST", "/job_groups/list", "List groups.", body={"pageNumber": 1, "pageSize": 20}),
                E("POST", "/job_groups/status_history", "Group status history.", body={"jobGroupId": 10, "pageNumber": 1, "pageSize": 20}),
                E("POST", "/job_groups/job_group_results_as_complete", "Mark complete.", body={"jobGroupId": 10}),
                E("POST", "/job_groups/job_group_results_as_financially_complete", "Mark financially complete.", body={"jobGroupId": 10}),
            ]),
            ("Job types", "Job type catalogue.", [
                E("POST", "/job_types/job_types", "Get type.", body={"jobTypeId": 42}),
                E("POST", "/job_types/list", "List types.", body={"pageNumber": 1, "pageSize": 100}),
            ]),
        ],
        COMMON,
    ),
    "invoices": page("Invoices", "BigChange invoices and line items", [
        ("Invoices", "Billing.", [
            E("GET", "/invoices/invoice", "Get invoice.", query=[("invoiceId", "5001")]),
            E("POST", "/invoices/create", "Create invoice.", body={"contactId": 12345, "createdAt": "2026-04-01T00:00:00Z"}),
            E("POST", "/invoices/edit", "Update invoice.", body={"invoiceId": 5001}),
            E("POST", "/invoices/list", "List invoices.", body={"pageNumber": 1, "pageSize": 50, "contactId": 12345}),
            E("POST", "/invoices/cancel", "Cancel.", body={"invoiceId": 5001}),
            E("POST", "/invoices/mark_paid", "Mark paid.", body={"invoiceId": 5001, "paidAt": "2026-04-15T12:00:00Z"}),
            E("POST", "/invoices/mark_sent", "Mark sent.", body={"invoiceId": 5001, "sentAt": "2026-04-10T09:00:00Z"}),
            E("POST", "/invoices/document/create", "Generate PDF.", body={"invoiceId": 5001}),
        ]),
        ("Invoice line items", "Line-level charges.", [
            E("GET", "/invoices/line_item", "Get line.", query=[("invoiceId", "5001"), ("lineItemId", "1")]),
            E("GET", "/invoices/line_item/edit", "Update line.", query=[("invoiceId", "5001"), ("lineItemId", "1")]),
            E("POST", "/invoices/line_item/create", "Create line.", body={"invoiceId": 5001, "description": "Labour", "quantity": 2, "unitSellingPrice": 85}),
            E("POST", "/invoices/line_item/delete", "Delete line.", body={"invoiceId": 5001, "lineItemId": 1}),
            E("POST", "/invoices/line_item/list", "List lines.", body={"invoiceId": 5001, "pageNumber": 1, "pageSize": 50}),
        ]),
    ], COMMON),
    "quotes": page("Quotes", "BigChange quotes and line items", [
        ("Quotes", "Quotations.", [
            E("GET", "/quotes/quote", "Get quote.", query=[("quoteId", "3001")]),
            E("POST", "/quotes/create", "Create quote.", body={"contactId": 12345}),
            E("POST", "/quotes/edit", "Update quote.", body={"quoteId": 3001}),
            E("POST", "/quotes/list", "List quotes.", body={"pageNumber": 1, "pageSize": 50}),
            E("POST", "/quotes/mark_sent", "Mark sent.", body={"quoteId": 3001}),
            E("POST", "/quotes/mark_accepted", "Mark accepted.", body={"quoteId": 3001}),
            E("POST", "/quotes/mark_rejected", "Mark rejected.", body={"quoteId": 3001}),
        ]),
        ("Quote line items", "Quote lines.", [
            E("GET", "/quotes/line_item", "Get line.", query=[("quoteId", "3001"), ("lineItemId", "1")]),
            E("POST", "/quotes/line_item/create", "Create line.", body={"quoteId": 3001, "description": "Boiler service", "quantity": 1}),
            E("POST", "/quotes/line_item/edit", "Update line.", body={"quoteId": 3001, "lineItemId": 1}),
            E("POST", "/quotes/line_item/delete", "Delete line.", body={"quoteId": 3001, "lineItemId": 1}),
            E("POST", "/quotes/line_item/list", "List lines.", body={"quoteId": 3001, "pageNumber": 1, "pageSize": 50}),
        ]),
    ], COMMON),
    "sales-opportunities": page("Sales Opportunities", "Pipeline and line items", [
        ("Sales opportunities", "CRM pipeline.", [
            E("GET", "/sales_opportunities/sales_opportunity", "Get opportunity.", query=[("id", "2001")]),
            E("POST", "/sales_opportunities/list", "List (filter required).", body={"contactId": 12345, "pageNumber": 1, "pageSize": 50}),
            E("POST", "/sales_opportunities/edit", "Update.", body={"id": 2001}),
            E("POST", "/sales_opportunities/probabilities/list", "List probabilities.", body={"pageNumber": 1, "pageSize": 50}),
            E("POST", "/sales_opportunities/stages/list", "List stages.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
        ("Line items", "Opportunity lines.", [
            E("GET", "/sales_opportunities/line_item", "Get line.", query=[("salesOpportunityId", "2001"), ("id", "1")]),
            E("POST", "/sales_opportunities/line_item/list", "List lines.", body={"salesOpportunityId": 2001, "pageNumber": 1, "pageSize": 50}),
            E("POST", "/sales_opportunities/line_item/create", "Create line.", body={"salesOpportunityId": 2001}),
            E("POST", "/sales_opportunities/line_item/edit", "Update line.", body={"salesOpportunityId": 2001, "id": 1}),
            E("POST", "/sales_opportunities/line_item/delete", "Delete line.", body={"salesOpportunityId": 2001, "id": 1}),
        ]),
    ], COMMON),
    "purchase-orders": page("Purchase Orders", "POs, series, and lines", [
        ("Purchase orders", "Procurement.", [
            E("GET", "/purchase_orders/purchase_order", "Get PO.", query=[("id", "4001")]),
            E("POST", "/purchase_orders/create", "Create PO.", body={"supplierId": 999, "contactId": 12345}),
            E("POST", "/purchase_orders/edit", "Update PO.", body={"id": 4001}),
            E("POST", "/purchase_orders/list", "List (filter required).", body={"jobId": 12345, "pageNumber": 1, "pageSize": 50}),
            E("POST", "/purchase_orders/series/list", "List series.", body={"pageNumber": 1, "pageSize": 50}),
            E("GET", "/purchase_orders/series", "Get series.", query=[("id", "10")]),
        ]),
        ("Line items", "PO lines.", [
            E("GET", "/purchase_orders/line_item", "Get line.", query=[("purchaseOrderId", "4001"), ("id", "1")]),
            E("POST", "/purchase_orders/line_item/list", "List lines.", body={"purchaseOrderId": 4001, "pageNumber": 1, "pageSize": 50}),
            E("POST", "/purchase_orders/line_item/create", "Create line.", body={"purchaseOrderId": 4001}),
            E("POST", "/purchase_orders/line_item/edit", "Update line.", body={"purchaseOrderId": 4001, "id": 1}),
            E("POST", "/purchase_orders/line_item/delete", "Delete line.", body={"purchaseOrderId": 4001, "id": 1}),
        ]),
    ], COMMON),
    "notes": page("Notes", "Notes and note types", [
        ("Notes", "Entity notes.", [
            E("GET", "/notes/note", "Get note.", query=[("id", "7001")]),
            E("POST", "/notes/create", "Create note.", body={"entityType": "job", "entityId": 12345, "typeId": 1, "subject": "Follow-up"},
              enums={"entityType": ["contact", "job", "resource", "stockItem", "vehicle", "salesOpportunity", "contract"]}),
            E("POST", "/notes/edit", "Update note.", body={"noteId": 7001, "subject": "Updated"}),
            E("POST", "/notes/list", "List notes.", body={"entityType": "job", "entityId": 12345, "status": "open", "pageNumber": 1, "pageSize": 50},
              enums={"status": ["open", "completed", "cancelled"]}),
            E("POST", "/notes/progress_update", "Update progress.", body={"noteId": 7001, "percentage": 50}),
        ]),
        ("Note types", "Note type definitions.", [
            E("GET", "/note_types/note", "Get type.", query=[("noteTypeId", "1")]),
            E("POST", "/note_types/list", "List types.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
    ], COMMON),
    "persons": page("Persons", "Site contacts and consent", [
        ("Persons", "People on accounts.", [
            E("GET", "/persons/person", "Get person.", query=[("personId", "550e8400-e29b-41d4-a716-446655440000")]),
            E("POST", "/persons/create", "Create person.", body={"contactId": 12345, "firstName": "Jane", "surname": "Smith", "email": "jane@example.com"}),
            E("POST", "/persons/edit", "Update person.", body={"personId": "550e8400-e29b-41d4-a716-446655440000"}),
            E("POST", "/persons/list", "List persons.", body={"contactId": 12345, "pageNumber": 1, "pageSize": 25}),
            E("POST", "/persons/consent/set", "Set consent.", body={"personId": "550e8400-e29b-41d4-a716-446655440000", "status": "granted", "medium": "email"},
              enums={"status": ["awaiting", "refused", "granted"], "medium": ["email", "click", "telephone"]}),
            E("POST", "/persons/consent/history", "Consent history.", body={"personId": "550e8400-e29b-41d4-a716-446655440000", "pageNumber": 1, "pageSize": 20}),
        ]),
    ], COMMON),
    "resources": page("Resources", "Engineers and resource groups", [
        ("Resources", "Engineers/technicians.", [
            E("GET", "/resources/resource_get", "Get resource.", query=[("resourceId", "100")]),
            E("POST", "/resources/resource_create", "Create resource.", body={"name": "Alex Engineer", "groupId": 5}),
            E("POST", "/resources/update", "Update resource.", body={"resourceId": 100, "name": "Alex Engineer"}),
            E("POST", "/resources/resources_list", "List resources.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
        ("Resource groups", "Teams.", [
            E("GET", "/resource_groups/resource_group/get", "Get group.", query=[("resourceGroupId", "5")]),
            E("POST", "/resource_groups/list", "List groups.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
    ], COMMON),
    "vehicles": page("Vehicles", "Fleet vehicles", [
        ("Vehicles", "Fleet.", [
            E("GET", "/vehicles/vehicle_get", "Get vehicle.", query=[("vehicleId", "50")]),
            E("POST", "/vehicles/create", "Create vehicle.", body={"registration": "AB12 CDE"}),
            E("POST", "/vehicles/update", "Update vehicle.", body={"vehicleId": 50}),
            E("POST", "/vehicles/list", "List vehicles.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
    ], COMMON),
    "stock": page("Stock", "Inventory, movements, suppliers", [
        ("Stock details", "Product catalogue.", [
            E("GET", "/stock/stock_details", "Get details.", query=[("stockDetailsId", "10")]),
            E("POST", "/stock/stock_details_create", "Create details.", body={"model": "Thermostat T100"}),
            E("POST", "/stock/stock_details_update", "Update details.", body={"stockDetailsId": 10}),
            E("POST", "/stock/stock_details_list", "List details.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
        ("Stock items", "Physical stock.", [
            E("GET", "/stock/stock/item_get", "Get item.", query=[("stockItemId", "20")]),
            E("POST", "/stock/stock_item_create", "Create item.", body={"stockDetailsId": 10, "quantity": 5}),
            E("POST", "/stock/stock_item_update", "Update item.", body={"stockItemId": 20}),
            E("POST", "/stock/stock_item_list", "List items.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
        ("Movements", "Stock movements.", [
            E("POST", "/stock/stock_movements_list", "List movements.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
        ("Product categories", "Categories.", [
            E("GET", "/stock/product_categories/get", "Get category.", query=[("productCategoryId", "3")]),
            E("POST", "/stock/product_categories_list", "List categories.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
        ("Suppliers", "Stock suppliers.", [
            E("GET", "/stock/stock_supplier_get", "Get supplier.", query=[("id", "1")]),
            E("POST", "/stock/stock_supplier_create", "Add supplier.", body={"stockDetailsId": 10, "contactId": 999}),
            E("POST", "/stock/stock_supplier_update", "Update supplier.", body={"id": 1}),
            E("POST", "/stock/stock_supplier_list", "List suppliers.", body={"stockDetailsId": 10, "pageNumber": 1, "pageSize": 20}),
        ]),
    ], COMMON + "\n\nNote: path `/stock/stock/item_get` is correct — the segment `stock` appears twice in the BigChange route, not a documentation typo."),
    "worksheets": page("Worksheets", "Forms and answers", [
        ("Worksheets", "Digital forms.", [
            E("GET", "/worksheet/worksheet_get", "Get worksheet.", query=[("worksheetId", "1")]),
            E("POST", "/worksheet/worksheet_list", "List worksheets.", body={"pageNumber": 1, "pageSize": 50}),
            E("POST", "/worksheet/worksheet_questions_get", "Get questions.", body={"worksheetId": 1, "pageNumber": 1, "pageSize": 100}),
            E("POST", "/worksheet/worksheet_answers_list", "List answers.", body={"worksheetId": 1, "pageNumber": 1, "pageSize": 50}),
        ]),
        ("Worksheet groups", "Form groups.", [
            E("GET", "/worksheet_groups/worksheet_group_get", "Get group.", query=[("worksheetGroupId", "1")]),
            E("POST", "/worksheet_groups/worksheet_group_list", "List groups.", body={"pageNumber": 1, "pageSize": 50}),
        ]),
    ], COMMON),
    "reference-data": page("Reference Data", "Department and nominal codes", [
        ("Department codes", "Departments.", [
            E("POST", "/reference_data/department_codes_list", "List codes.", body={"pageNumber": 1, "pageSize": 100}),
            E("GET", "/reference_data/retrieves_details", "Get code.", query=[("departmentCodeId", "1")]),
        ]),
        ("Nominal codes", "Nominal accounts.", [
            E("POST", "/reference_data/normalt_codes_list", "List codes.", body={"pageNumber": 1, "pageSize": 100}),
            E("GET", "/reference_data/nominal_code_id", "Get code.", query=[("nominalCodeId", "1")]),
        ]),
    ], COMMON),
}


def main():
    for name, content in PAGES.items():
        path = OUT / f"{name}.mdx"
        path.write_text(content, encoding="utf-8")
        n = content.count("### `")
        print(f"wrote {path.name}: {n} endpoints")


if __name__ == "__main__":
    main()
