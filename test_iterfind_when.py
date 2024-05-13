from pyteomics import mzid
from pyteomics.xml import _local_name
from lxml import etree
from memory_profiler import profile
import time

def iterfind_when(source, target_name, condition_name, stack_predicate, **kwargs):
    """
    Iteratively parse XML stream in ``source``, yielding XML elements
    matching ``target_name`` as long as earlier in the tree a ``condition_name`` element
    satisfies ``stack_predicate``, a callable that takes a single :class:`etree.Element` and returns
    a :class:`bool`.

    Parameters
    ----------
    source: file-like
        A file-like object over an XML document
    target_name: str
        The name of the XML tag to parse until
    condition_name: str
        The name to start parsing at when `stack_predicate` evaluates to true on this element.
    stack_predicate: callable
        A function called with a single `etree.Element` that determines if the sub-tree should be parsed
    **kwargs:
        Additional arguments passed to :meth:`source._get_info_smart`

    Yields
    ------
    lxml.etree.Element
    """
    g = etree.iterparse(source, ("start", "end"))
    state = False
    history = []
    for event, tag in g:
        lc_name = _local_name(tag)
        if event == "start":
            if lc_name == condition_name:
                state = stack_predicate(tag)
        else:
            if lc_name == target_name and state:
                value = source._get_info_smart(tag, **kwargs)
                for t in history:
                    t.clear()
                history.clear()
                yield value
            elif state:
                history.append(tag)
            elif not state:
                tag.clear()


# @profile
def test3():
    reader = mzid.MzIdentML("multiple_spectra_per_id_1_3_0_draft.mzid", retrieve_refs=False, use_index=True)
    sil_ids = list(reader.index['SpectrumIdentificationList'].keys())
    for sil_id in sil_ids:
        print("Processing SpectrumIdentificationList", sil_id)
        # do something
        # print(sir)
        reader.reset()
        for e in iterfind_when(
                reader,
                "SpectrumIdentificationResult",
                "SpectrumIdentificationList",
                lambda x: x.attrib["id"] == sil_id,
                retrieve_refs=False
        ):
            try:
                e['SpectrumIdentificationItem']
                print(f"Has SpectrumIdentificationItem?: {e['SpectrumIdentificationItem']}")
            except KeyError:
                print(f"Has no SpectrumIdentificationItem?: {e}")
        pass
    print("Test 3 done!")


print("Test 3 - iter when")
# log timing info
start = time.time()
test3()
end = time.time()
print(f"Time taken: {end - start}")
