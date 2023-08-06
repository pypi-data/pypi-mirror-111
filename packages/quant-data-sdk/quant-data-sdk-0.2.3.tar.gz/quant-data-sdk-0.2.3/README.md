# QuantData sdk

# auth token

    for access write to support@quantdata.science

# simple usage:

    get companies:

        api = QuantumDataApi(API_TOKEN)
        response = api.get_companies()


    get quotations:
    
        api = QuantumDataApi(API_TOKEN)
        response = api.get_quotations_as_df("KGHM", date_from="2015-01-01", date_to="2021-01-01", stock="GPW")

    get reports:

        api = QuantumDataApi(API_TOKEN)
        response = api.get_reports("KGHM")
