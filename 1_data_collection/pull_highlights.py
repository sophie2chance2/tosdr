import pandas as pd
import data_func

# import importlib
# importlib.reload(data_func)
# importlib.reload(browser_login)

# get the list of services
services_df = data_func.get_services(num_pages = 5)
reviewed_services_df = services_df[services_df['is_comprehensively_reviewed']==True] # filter for services that have been reviewed
reviewed_services_df = reviewed_services_df.reset_index(drop=True)
# reviewed_services_df.to_csv('reviewed_services.csv', index=False)
services_df.to_csv('raw_data/services.csv', index=False)


######################## LIMIT SERVICES PULLED FOR TESTING ########################
# reviewed_services_df = reviewed_services_df.head(1)
reviewed_services_df = services_df[9:10].reset_index(drop=True)
##################################################################################

# pull highlights from each of the services
all_highlights = pd.DataFrame()
for i in range(len(reviewed_services_df)):
    service = reviewed_services_df['slug'][i]
    highlight_labels_df = data_func.pull_highlight_labels(service)
    highlight_labels_df['service_id'] = reviewed_services_df['id'][i]
    highlight_labels_df['service_name'] = reviewed_services_df['name'][i]
    all_highlights = pd.concat([all_highlights, highlight_labels_df], ignore_index=True)
    all_highlights.loc[i, 'service_id'] = reviewed_services_df['id'][i]
    all_highlights.loc[i, 'service_name'] = reviewed_services_df['name'][i]
    print(f"{service} highlights complete")

all_highlights.rename(columns={'id': 'highlight_id', 'discussion':'highlight_link', 'quoteDoc':'segment_name', 'title': 'paraphrase'}, inplace=True)

# reindex
all_highlights_final = all_highlights.reindex(['service_id', 'service_name', 'paraphrase', 'highlight_id', 'highlight', 'highlight_link', 'segment_name'], axis=1)
all_highlights_final.to_csv('raw_data/highlights.csv', index=False)


data_func.pull_highlight_labels('1557')