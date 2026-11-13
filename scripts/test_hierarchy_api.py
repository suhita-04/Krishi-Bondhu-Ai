import urllib.request
import json

def test():
    res = urllib.request.urlopen('http://127.0.0.1:8000/api/hierarchy')
    data = json.loads(res.read().decode('utf-8'))
    districts = data.get('districts', {})
    print(f"Total Districts: {len(districts)}")

    for d_id, d_data in districts.items():
        upz_keys = list(d_data.get('upazilas', {}).keys())
        sample_upz = upz_keys[0]
        sample_union = d_data['upazilas'][sample_upz]['unions'][0]
        
        req_body = {
            'region_id': d_id,
            'upazila': sample_upz,
            'union_id': sample_union['id'],
            'union_name': sample_union['name_en'],
            'past_crop': 'boro_rice'
        }
        req = urllib.request.Request(
            'http://127.0.0.1:8000/api/analyze',
            data=json.dumps(req_body).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        res_a = urllib.request.urlopen(req)
        a_data = json.loads(res_a.read().decode('utf-8'))
        prof = a_data['district_profile']
        print(f"✓ {d_data['name_bn']} ({d_id}): {len(upz_keys)} upazilas, Union: {sample_union['name_bn']} (Elev: {prof['elevation_m']}m, Basin: {prof['river_basin']})")

if __name__ == "__main__":
    test()

