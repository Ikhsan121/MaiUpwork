from bs4 import BeautifulSoup
import re


# this function return list of dictionary for asn object
def asn_object(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    rows = main_content.find_all('tr')
    column1_data = []
    column2_data = []
    for row in rows:
        # ignore header column
        if row.find('table'):
            continue
        cells = row.find_all('td')
        # make sure each row has at least two column
        if len(cells) >= 2:
            # Extract the content from the first and second cell and append to the respective lists
            column1_data.append(re.sub(r"\s+", " ", cells[0].text.strip()).replace("Handle", "ASN Handle"))
            column2_data.append(re.sub(r"\s+", " ", cells[1].text.strip()))
            # adding column org handle
            if re.sub(r"\s+", " ", cells[0].text.strip()) == 'Organization':
                column1_data.append('Org Handle')
                column2_data.append(re.sub(r"\s+", " ", cells[1].text.strip()).split("(")[1].replace(")", ""))

    # create dict
    data = {}
    for key, value in zip(column1_data, column2_data):
        if key not in data:
            data[key] = []
        data[key].append(value)
    # delete see also key
    data = {k: v for k, v in data.items() if k != "See Also"}

    return data



def org_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    rows = main_content.find_all('tr')
    column1_data = []
    column2_data = []
    for row in rows:
        # ignore header column
        if row.find('table'):
            continue
        cells = row.find_all('td')
        # make sure each row has at least two column
        if len(cells) >= 2:
            # Extract the content from the first and second cell and append to the respective lists
            column1_data.append(re.sub(r"\s+", " ", cells[0].text.strip()))
            column2_data.append(cells[1])

    # create dict
    data = {}
    for key, value in zip(column1_data, column2_data):
        if key not in data:
            data[key] = []
        data[key].append(value)
    # delete see also key
    data = {k: v for k, v in data.items() if k != "See Also"}
    # Get the value associated with 'Organization'
    organization_data = "<html>" + str(data['Organization'][0]) + "</html>"
    # Parse the HTML element using BeautifulSoup
    soup = BeautifulSoup(organization_data, 'html.parser')
    link = soup.find('a').get('href')
    return link


def org_object(html_content, asn):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    rows = main_content.find_all('tr')
    column1_data = []
    column2_data = []
    for row in rows:
        # ignore header column
        if row.find('table'):
            continue
        cells = row.find_all('td')
        # make sure each row has at least two column
        if len(cells) >= 2:
            # Extract the content from the first and second cell and append to the respective lists
            column1_data.append(re.sub(r"\s+", " ", cells[0].text.strip()).replace("Handle", "Org Handle"))
            column2_data.append(re.sub(r"\s+", " ", cells[1].text.strip()))
    # create asn column
    column1_data.append("ASN Handle")
    column2_data.append(asn)
    # create dict
    data = {}
    for key, value in zip(column1_data, column2_data):
        if key not in data:
            data[key] = []
        data[key].append(value)
    return data


# poc_link return a list of poc links
def poc_link(html_content):
    link_list = []
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    links = main_content.find_all('a')
    for link in links:
        link_list.append(link['href'])
    return link_list


# poc_object function return dictionary of the table
def poc_object(html_content, org_data):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    rows = main_content.find_all('tr')
    column1_data = []
    column2_data = []
    for row in rows:
        # ignore header column
        if row.find('table'):
            continue
        cells = row.find_all('td')
        # make sure each row has at least two column
        if len(cells) >= 2:
            # Extract the content from the first and second cell and append to the respective lists
            column1_data.append(re.sub(r"\s+", " ", cells[0].text.strip()).replace("Handle", "POC Handle"))
            column2_data.append(re.sub(r"\s+", " ", cells[1].text.strip()))
    # adding unique org handle
    column1_data.append("Org Handle")
    column2_data.append(org_data['Org Handle'][0])
    # create dict
    data = {}
    for key, value in zip(column1_data, column2_data):
        if key not in data:
            data[key] = []
        data[key].append(value)
    # delete see also key
    data = {k: v for k, v in data.items() if k != "See Also"}
    return data


#  net_object function return dictionary of the table
def net_object(html_content, org_handle):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    rows = main_content.find_all('tr')
    column1_data = []
    column2_data = []
    for row in rows:
        # ignore header column
        if row.find('table'):
            continue
        cells = row.find_all('td')
        # make sure each row has at least two column
        if len(cells) >= 2:
            # Extract the content from the first and second cell and append to the respective lists
            column1_data.append(re.sub(r"\s+", " ", cells[0].text.strip()))
            column2_data.append(re.sub(r"\s+", " ", cells[1].text.strip()))
    # adding unique org Handle
    organization_handle = org_handle['Org Handle'][0]
    column3_data = [organization_handle]*len(column1_data)
    # create dict
    data = {
        'Net': column1_data,
        'IP Range': column2_data,
        'Org Handle': column3_data
    }

    return data


# net_link return a list of net links
def net_link(html_content):
    link_list = []
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    links = main_content.find_all('a')
    for link in links:
        link_list.append(link['href'])
    return link_list


def net_resource_object(html_content, org_data):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', attrs={'id': 'maincontent'}).find('table')
    rows = main_content.find_all('tr')
    column1_data = []
    column2_data = []
    for row in rows:
        # ignore header column
        if row.find('table'):
            continue
        cells = row.find_all('td')
        # make sure each row has at least two column
        if len(cells) >= 2:
            # Extract the content from the first and second cell and append to the respective lists
            column1_data.append(re.sub(r"\s+", " ", cells[0].text.strip()).replace("Handle", "Net Handle"))
            column2_data.append(re.sub(r"\s+", " ", cells[1].text.strip()))
    # adding unique org handle
    column1_data.append("Org Handle")
    column2_data.append(org_data['Org Handle'][0])
    # create dict
    data = {}
    for key, value in zip(column1_data, column2_data):
        if key not in data:
            data[key] = []
        data[key].append(value)
    # delete see also key
    data = {k: v for k, v in data.items() if k != "See Also"}
    return data

