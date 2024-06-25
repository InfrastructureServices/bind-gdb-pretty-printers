all: gen_dirs

gen_dirs:
	for D in dns_name dns_rdataclass dns_rdatatype; do \
		(cd $$D && ./gen_json_dict.py); \
	done

dns_name/nameattr_dict.json: dns_name/gen_json_dict.py
	cd dns_name && ./gen_json_dict.py

dns_rdataclass/nameattr_dict.json: dns_rdataclass/gen_json_dict.py
	cd dns_name && ./gen_json_dict.py
	
dns_rdatatype/nameattr_dict.json: dns_rdatatype/gen_json_dict.py
	cd dns_name && ./gen_json_dict.py
