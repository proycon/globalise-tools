#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from typing import List

import cassis as cas
from icecream import ic
from loguru import logger


class XMIProcessor:

    def __init__(self, typesystem, xmi_path: str):
        self.typesystem = typesystem
        self.xmi_path = xmi_path
        logger.info(f"<= {xmi_path}")
        with open(xmi_path, 'rb') as f:
            self.cas = cas.load_cas_from_xmi(f, typesystem=self.typesystem)

    def get_sofa_string(self) -> str:
        return self.cas.get_sofa().sofaString

    def get_named_entity_annotations(self):
        return [self._as_web_annotation(a) for a in self.cas.views[0].get_all_annotations() if
                a.type.name == "de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"]
        # return [a for a in cas.views[0].get_all_annotations() if a.type.name=="de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"]

    @staticmethod
    def _get_prefix(a) -> str:
        return ""

    @staticmethod
    def _get_suffix(a) -> str:
        return ""

    def _as_web_annotation(self, nea):
        anno_id = f"urn:globalise:annotation:{nea.xmiID}"
        text_quote_selector = {
            "type": "TextQuoteSelector",
            "exact": nea.get_covered_text()
        }
        prefix = self._get_prefix(nea)
        if prefix:
            text_quote_selector['prefix'] = prefix
        suffix = self._get_suffix(nea)
        if suffix:
            text_quote_selector['suffix'] = suffix
        return {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": anno_id,
            "type": "Annotation",
            "motivation": "tagging",
            "generated": datetime.today().isoformat(),
            "body": f"https://digitaalerfgoed.poolparty.biz/globalise/annotation/ner/{nea.value}",
            "target": {
                "source": "urn:text",
                "selector": [
                    {
                        "type": "TextQuoteSelector",
                        "exact": nea.get_covered_text()
                    },
                    {
                        "type": "TextPositionSelector",
                        "start": nea.begin,
                        "end": nea.end
                    }
                ]
            }
        }


class XMIProcessorFactory:

    def __init__(self, typesystem_path: str):
        logger.info(f"<= {typesystem_path}")
        with open(typesystem_path, 'rb') as f:
            self.typesystem = cas.load_typesystem(f)

    def get_xmi_processor(self, xmi_path: str) -> XMIProcessor:
        return XMIProcessor(self.typesystem, xmi_path)


@logger.catch
def get_arguments():
    parser = argparse.ArgumentParser(
        description="Extract Web Annotations from XMI files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("xmi_path",
                        help="The XMI files to use",
                        type=str,
                        nargs='+'
                        )
    return parser.parse_args()


@logger.catch
def extract_web_annotations(xmi_paths: List[str]):
    base = '/Users/bram/workspaces/globalise'
    xpf = XMIProcessorFactory(f'{base}/globalise-tools/data/typesystem.xml')
    for xmi_path in xmi_paths:
        basename = xmi_path.split('/')[-1].replace('.xmi', '')
        xp = xpf.get_xmi_processor(xmi_path)
        nea = xp.get_named_entity_annotations()

        json_path = f"out/{basename}_web-annotations.json"
        logger.info(f"=> {json_path}")
        with open(json_path, 'w') as f:
            json.dump(nea, f)

        txt = xp.get_sofa_string()
        txt_path = f"out/basename}_plain-text.txt"
        logger.info(f"=> {txt_path}")
        with open(txt_path, 'w') as f:
            f.write(txt)


if __name__ == '__main__':
    args = get_arguments()
    if args.xmi_path:
        extract_web_annotations(args.xmi_path)
