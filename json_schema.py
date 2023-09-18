import json
from jsonschema import Draft7Validator
from jsonschema.validators import validator_for

def generate_json_schema(json_data):
    schema = {}

    def walk(current_data, current_schema):
        if isinstance(current_data, dict):
            current_schema['type'] = 'object'
            current_schema['properties'] = {}
            for key, value in current_data.items():
                current_schema['properties'][key] = {}
                walk(value, current_schema['properties'][key])
        elif isinstance(current_data, list):
            current_schema['type'] = 'array'
            current_schema['items'] = {}
            if len(current_data) > 0:
                walk(current_data[0], current_schema['items'])
        else:
            current_schema['type'] = 'string'

    walk(json_data, schema)
    return schema

# Exemplo de uso
json_data = {
	"nicename": "JSML36 - DEBÊNTURE JSL SA - 07/2020",
	"identifier": "jsml36:deb",
	"asset_type_mr": "DEBÊNTURES",
	"first_quote_date": "2013-11-04",
	"last_quote_date": "2020-07-15",
	"last_update": "2020-07-15",
	"has_quotes": True,
	"deb": {
		"ticker": "JSML36",
		"form": "Escritural",
		"standardized_deed": False,
		"serie": "003",
		"issuance": 6,
		"situation": "Excluído",
		"issuer_name": "JSL S.A",
		"early_redemption": False,
		"cnpj": 52548435000179,
		"tax_incentive_debenture": False,
		"isin": "BRJSLGDBS095",
		"issuance_date": "2013-07-15",
		"maturity_date": "2020-07-15",
		"collateral": "Quirografária",
		"class": "Simples",
		"indexer": "IPCA",
		"premium": "",
		"fees": "7.5% a.a. a cada 12 meses. Primeiro pagamento em 15/07/2014",
		"amortization": "50.0% a.a. a cada 12 meses. Primeiro pagamento em 15/07/2019"
	}
}

json_schema = generate_json_schema(json_data)

# Imprimir o esquema gerado
print(json.dumps(json_schema, indent=4))



