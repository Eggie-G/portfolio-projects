# save as src/run_queries.py (optional convenience)
import duckdb

con = duckdb.connect()
con.execute(open("ecommerce_query.sql","r",encoding="utf-8").read())