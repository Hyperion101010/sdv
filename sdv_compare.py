import json 
import yaml

# Load the contents of the given json, yaml and mapping file.
def load_file():
	try:
		with open('platform_description_18March2020.json','r') as f:
			json_file = json.load(f)
		with open('intel-pod10.yaml','r') as f:
			yaml_file = yaml.load(f, Loader=yaml.FullLoader)
		with open('mapping.txt','r') as f:
			mapping_file = f.read()
	except FileNotFoundError:
		print('File not found\n')
	except:
		print('Unexpected error\n')
	else:
		return json_file, yaml_file, mapping_file

# Convert mapping.txt entries to a list based lookup for easy iteration 
# while finding the respective key values.
def contruct_lkup(mapping_file):
	lkup = list()
	mapping_file = mapping_file.split('\n')
	for i in mapping_file:
		if i == "":
			continue
		else:			
			lkup.append(i.split(' : '))
	return lkup 	

# Recursively find the key value from the given file contents
# using Generator functions for low memory footprint returning
# iterator
def find(key, dictionary):
	for k, v in dictionary.items():
		if k==key:
			yield v
		elif isinstance(v, dict):
			for res in find(key, v):
				yield res
		elif isinstance(v, list):
			for d in v:
				for res in find(key, d):
					yield res

# Load the required files, iterate through the mapping
# entries using next() lookups for finding the key value.
if __name__=="__main__":
	json_file, yaml_file, mapping_file = load_file()
	mapping_list = contruct_lkup(mapping_file)
	for i in range(len(mapping_list)):
		json_k, yaml_k = mapping_list[i]
		try:
			json_v = find(json_k, json_file)
			json_v = next(json_v)
			yaml_v = find(yaml_k, yaml_file)
			yaml_v = next(yaml_v)
		except StopIteration:
			print('Not a valid key\n')
		except:
			print('Unexpected error\n')
		else:
			if json_v == yaml_v:
				print('Values matched for json key:', json_k,'\tyaml key:', yaml_k)
			else:
				print('Values not matched for json key:', json_k,'\tyaml key:', yaml_k)
