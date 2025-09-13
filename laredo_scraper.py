


scrape_count = {}


while idx < total:
try:
county_name = self.driver.find_elements(By.XPATH, '//span[contains(@class, "county-name")]')[idx].text
county_slug = slugify(county_name)
print(f"Scraping {county_name}")


count = scrape_count.get(idx, 0)
second_pass = (count == 1) and (idx in rescrape_indices)


if self._connect_county(county_name, idx):
self._close_popup()
self._fill_form(county_name, second_pass=second_pass)
intercepted = self._intercept_after_search()
docs_list = intercepted.get("docs_list", [])
auth_token = intercepted.get("auth_token", "")


cleaned = self._clean_results(county_slug, docs_list)
if cleaned:
grouped = self._group_by_doc_number(cleaned)
id_map = self._id_map(docs_list)
combined = self._combine_records(auth_token, id_map, grouped)
if combined:
stem = f"{county_slug}_resolution" if second_pass else county_slug
self._write_json(combined, stem)
self.combined_records_all.extend(combined)
self.flow_log.setdefault(county_name, {})["data_json"] = "saved"
else:
print(f"No combined records for '{county_name}'")
self.flow_log.setdefault(county_name, {})["data_json"] = "empty"
self._disconnect(county_name)


scrape_count[idx] = count + 1
if idx in rescrape_indices and scrape_count[idx] == 1:
print(f"Re-scraping {county_name} for second pass")
continue # same idx again
idx += 1


except Exception as e:
self._write_log(f"iterate counties error: {e}")
idx += 1


counties = self._counties()
total = len(counties)


# write combined file
if self.combined_records_all:
self._write_json(self.combined_records_all, "all_counties")


self._logout()
self.driver.quit()
self.flow_log["time_taken_sec"] = round(time.time() - self.flow_start_time, 2)
self._write_flow_logs()
except Exception as e:
self._write_log(f"run() error: {e}")
try:
self.driver.quit()
except Exception:
pass




if __name__ == "__main__":
parser = argparse.ArgumentParser(description="Laredo scraper -> JSON")
parser.add_argument("--out", default="files", help="Output directory")
parser.add_argument("--headless", action="store_true", help="Run in headless mode")
parser.add_argument("--wait", type=int, default=10, help="Wait seconds for UI elements")
parser.add_argument("--max-parties", type=int, default=6, help="How many Party columns to expose (Party1..PartyN)")
parser.add_argument("--rescrape-indices", nargs='*', type=int, default=[1, 2], help="County indices to scrape twice")
args = parser.parse_args()


scraper = LaredoScraper(out_dir=args.out, headless=args.headless, wait_seconds=args.wait, max_parties=args.max_parties)
scraper.run(rescrape_indices=set(args.rescrape_indices))
