
from src.helpers.logger import logger
from json import dumps, loads
from src.domain.model import Website, CheckResult, WebStatus, WebsiteReport

def summary_maker(reports):
  up_websites = []
  down_websites = []
  degraded_websites = []
  unkown_websites = []
  
  web_count = 0
  up_count = 0
  down_count = 0
  degraded_count = 0
  unknown_count = 0

  for report in reports:
    try:
      if report.website:
        web_count += 1
        if report.status == "UP":
          up_count += 1
          up_websites.append(report.website.URL)
        elif report.status == "DOWN":
          down_count += 1
          down_websites.append(report.website.URL)
        elif report.status == "DEGRADED":
          degraded_count += 1
          degraded_websites.append(report.website.URL)
        elif report.status == "UNKNOWN":
          unknown_count += 1
          unkown_websites.append(report.website.URL)
    except AttributeError as e:
      logger.error(f"{report} : {e}")
  report_file = "./reports/report.txt"
  
  with open(report_file, 'w') as file:
    file.write("Report Summary")
    file.write("\n")
    file.write("----------------------")
    file.write("\n")
    file.write("\n")

    file.write(f"Total: {web_count} \n")
    file.write(f"UP: {up_count} \n")
    file.write(f"DOWN: {down_count} \n")
    file.write(f"DEGRADED: {degraded_count} \n")
    if unknown_count != 0:
      file.write(f"UNKNOWN: {unknown_count} \n")
    
    file.write("\n")
    if up_count != 0:
      file.write("UP")
      file.write("\n")
      for website in up_websites:
        file.write(f"- {website} \n")
      
    file.write("\n")
    if down_count != 0:
      file.write("DOWN")
      file.write("\n")
      for website in down_websites:
        file.write(f"- {website} \n")
    
    file.write("\n")
    if degraded_count != 0:
      file.write("DEGRADED")
      file.write("\n")
      for website in degraded_websites:
        file.write(f"- {website} \n")
    
    file.write("\n")
    if unknown_count != 0:
      file.write("UNKNOWN")
      file.write("\n")
      for website in unknown_websites:
        file.write(f"- {website} \n")
  return 