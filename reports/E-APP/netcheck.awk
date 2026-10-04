# Requires gawk (FPAT). Usage: gawk -f reports/E-APP/netcheck.awk <csv>
# Classify each row's net_sales column against candidate formulas (cents, exact).
# Uses FPAT to handle quoted commas. Columns located by header name.
BEGIN { FPAT = "([^,]*)|(\"[^\"]*\")" }
NR==1 { for (i=1;i<=NF;i++) c[$i]=i; next }
{
  g=sprintf("%.0f",$c["gross_sales"]*100); s=sprintf("%.0f",$c["shipping_collected"]*100)
  r=sprintf("%.0f",$c["refund_amount"]*100); n=sprintf("%.0f",$c["net_sales"]*100)
  rows++
  if (n==g-r) a++; if (n==g+s-r) b++; if (n==g-r && n==g+s-r) both++
}
END { printf "%s rows=%d  net==gross-refund:%d  net==gross+ship-refund:%d  ambiguous(ship=0):%d\n", FILENAME, rows, a, b, both }
