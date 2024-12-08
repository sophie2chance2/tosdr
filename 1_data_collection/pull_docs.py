import pandas as pd
import time
import random

import data_func
import browser_login

# get the list of services from the CSV - NOT PULLING FROM API
services_df = pd.read_csv('raw_data/services.csv')
reviewed_services_df = services_df[services_df['is_comprehensively_reviewed']==True] # filter for services that have been reviewed
reviewed_services_df = reviewed_services_df.reset_index(drop=True)

print(f"Number of reviewed services: {len(reviewed_services_df)}")
print(reviewed_services_df.head())

######################## LIMIT SERVICES PULLED FOR TESTING ########################
# reviewed_services_df = reviewed_services_df.head(2)
##################################################################################

### Pulling the Terms of Service
session = browser_login.create_session()
session_id = session['id']
# browser_login.create_debug_url(session_id) # Print the debug URL to observe the browser in action
print(f"Session: https://www.browserbase.com/sessions/{session_id}")

# Add in for loop here
all_service_docs = pd.DataFrame()
count = 0

for service_id in reviewed_services_df['id']:
    content, browser = browser_login.connect_to_browser(session_id, service_id)

    docs_labels = data_func.find_doc_id_names(content)
    docs_dict = data_func.get_docs(content)

    if docs_labels is None:
        print(f"Service {service_id} has no documents")
        continue

    # put data into a DataFrame
    data = []
    for doc_type, doc_id in docs_labels.items():
        clean_doc_id = doc_id.strip('#')
        doc_text = docs_dict.get(clean_doc_id, '')  # Get the doc text from docs_dict, default to empty string if not found
        data.append((clean_doc_id, doc_type, doc_text))

    # Create DataFrame from the data
    service_docs_df = pd.DataFrame(data, columns=['doc_id', 'doc_type', 'doc_text'])
    service_docs_df['service_id'] = service_id
    service_docs_df['segment_link'] = f"https://edit.tosdr.org/services/{service_id}/annotate"

    all_service_docs = pd.concat([all_service_docs, service_docs_df], ignore_index=True)

    # Every 10 services, save the data to a CSV
    if count % 10 == 0:
        all_service_docs.to_csv('raw_data/tos.csv', index=False)
        all_service_docs.to_excel('raw_data/tos.xlsx', index=False, engine='openpyxl')
        print(f"{count} docs saved")

    # print(all_service_docs)
    print(f"Service {service_id} docs retrieved")
    # Sleep for a random amount of time to prevent rate limiting
    time.sleep(random.uniform(2, 60))

    count += 1

all_service_docs.rename(columns={'doc_id': 'segment_id', 'doc_text': 'segment_text', 'doc_type':'segment_name'}, inplace=True)

all_service_docs.to_csv('raw_data/tos.csv', index=False)
all_service_docs.to_excel('raw_data/tos.xlsx', index=False, engine='openpyxl')