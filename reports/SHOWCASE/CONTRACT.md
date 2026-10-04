# GOV-03: Aimsigh showcase-v1 contract

Base /api/showcase/v1. JSON requests reject unknown keys. Every JSON response
contains contract_version="showcase-v1", synthetic=true. Money/ratios are decimal
strings, not binary floats; unknown values are null with availability_reason.
Existing /api/v1 and original metrics are unchanged.

GET /snapshot -> {snapshot_id,published_at,definition_version,sources:[{source,
metric_run_id,coverage:{state,covered_days,expected_days,missing_days},latest_import_state}],
auxiliary:[{input_id,kind,checksum,definition_version}],month:"2026-09"}.
Snapshot is immutable; GET returns the latest persisted snapshot, created only
when preparing or completing a collection. A prior snapshot remains addressable.

GET /metrics?snapshot_id=ID&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&source=all
&store=GW-001&platform=eBay -> {snapshot_id,scope:{start_date,end_date,source,
store,platform},coverage:{state,missing_days},freshness:{published_at,is_last_good},
metrics:[{metric_id,value,unit,availability,availability_reason,definition}],
daily:[{date,net_sales}],by_source:[{source,net_sales,records,orders}],
by_platform:[{platform,net_sales}],by_store:[{store,net_sales}],
customer_counts:[{source,platform,value,availability}],evidence_url,auxiliary_url}.
IDs: net_sales, labor_hours, revenue_per_labor_hour, contribution_margin,
contribution, fees, shipping_expense, labor_cost. Units USD, hours, USD/hour, percent.
Source defaults all; dates default Sep1–30. Empty store/platform means all.
Platform-selected labor-dependent metrics unavailable (no allocation).

GET /comparison with snapshot_id,source,store,platform -> {snapshot_id,previous:
metricsResponse,current:metricsResponse,explanation:string,verified_cause:false}.
Fixed Sep17–23 / Sep24–30; same filters throughout.
GET /evidence same scope parameters plus offset=0,limit=100 -> {snapshot_id,
scope,total_rows,rows:[{source,record_key,reporting_date,platform,store_id,buyer_id,
gross_item_sales,refunds,net_sales,fee,file_id,batch_id,source_row_number,metric_run_id}],
scope_total}.
GET /inputs same scope -> {snapshot_id,labor:[{source,date,store_id,minutes,
labor_cost,input_id,source_row_number}],shipping:[{source,record_key,amount,
input_id,source_row_number}],definitions:[string]}.
GET /sources -> {sources:[{name,kind,status,description}]} (nine report types).
GET /exports/workbook?snapshot_id=ID -> binary September XLSX.
GET /exports/sales.csv?snapshot_id=ID -> normalized month CSV.
GET /exports/dictionary?snapshot_id=ID -> JSON definitions/provenance.

POST /questions {snapshot_id,scope:{start_date,end_date,source,store,platform},
question:string} -> {snapshot_id,intent:"sales"|"evidence"|"productivity"|
"missing"|"unsupported",answer:string,tools:["metrics"|"comparison"|"evidence"],
citations:[{label,url}],comparison?:comparisonResponse,metrics?:metricsResponse}.
Supported intent matching uses deterministic normalized text; no models/messages.
GET /summary same scope -> same shape as question sales response, daily summary.
Chart attachment is a PNG generated in-browser from current plotted values.

POST /recordings {source:"upright_replica"|"cash_monkey_replica"} -> {recording_id,
source,status:"recording",events:[],recipe:null}.
POST /recordings/ID/events {event:{op:"navigate"|"click"|"fill"|"select"|
"ready"|"download",path:string,role?:string,name?:string,label?:string,value?:string,
observation:string}} -> recordingResponse. Max 25 actions; only local implemented
paths/controls. Dates are bound to start_date/end_date when compiling.
POST /recordings/ID/review {} -> recordingResponse with recipe and status review.
POST /recordings/ID/approve {} -> {recipe_id,source,recipe_version,approved:true,
recipe:existingSkillFormat}. Reviewed recipe includes report-ready/download steps.
GET /recipes -> {recipes:[approvedRecipeResponse]} (includes reviewed baseline
Upright and Cash Monkey skills so manual fallback remains available).

POST /runs {recipe_id,start_date,end_date,mode?:normal|session-expired|changed-label|
missing-report|delayed|timeout,headed?:boolean} -> {run_id,status,stage,source,
start_date,end_date,recipe_id,recipe_version,attempts:[],cause,owner_role,
batch_id:null,checksum:null,row_count:null,snapshot_id:null}.
GET /runs -> {runs:[runResponse],runtime_available:boolean}.
GET /runs/ID -> runResponse; terminal succeeded or needs_human. Status/stage:
pending/collecting/verifying/importing/complete/failed.
GET /runs/ID/events -> {events:[{step,op,detail,frame_url?:string}]}.
GET /runs/ID/frames/NAME.png -> actual Playwright screenshot bytes.

GET /showcase serves the UI; /showcase/assets/* controlled static files.
/showcase/portal/* proxies ONLY the configured loopback synthetic portal. Its
links/assets/API URLs honor the prefix and its iframe policy allows same origin.
UI recorder communicates with its exact iframe window, validates origin, and
uses a per-session nonce. No arbitrary remote destination/selector/script support.

GET /api/v1/inventory retains the separate August demonstration (never joined to
September sales). Existing /replica and / dashboard retain prior behavior.
