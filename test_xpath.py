from pyteomics import mzid

reader = mzid.MzIdentML("test.mzid", retrieve_refs=False)

sil_ids = list(reader.index['SpectrumIdentificationList'].keys())

for sil_id in sil_ids:
    print("Processing SpectrumIdentificationList", sil_id)
    reader.reset()
    xpath = f"//SpectrumIdentificationList[@id=\"{sil_id}\"]/*"
    print("XPATH: ", xpath)
    for sir in reader.iterfind(xpath):
        # do something
        print(sir)
print("Test 1 done!")

for sil_id in sil_ids:
    print("Processing SpectrumIdentificationList", sil_id)
    reader.reset()
    xpath = f"//SpectrumIdentificationList[@id=\"{sil_id}\"]/SpectrumIdentificationResult"
    print("XPATH: ", xpath)
    for sir in reader.iterfind(xpath):
        # do something
        print(sir)
print("Test 2 done!")
