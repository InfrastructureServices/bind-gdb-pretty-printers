GENERATED=dns_name dns_rdataclass dns_rdatatype

all: gen_dirs

gen_dirs:
	for D in $(GENERATED); do \
		(cd $$D && ./gen_json_dict.py) || exit $$?; \
	done
