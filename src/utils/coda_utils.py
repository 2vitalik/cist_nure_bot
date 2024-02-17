from shared_utils.api.coda.v2.doc import CodaDoc

import conf

doc = CodaDoc(conf.coda_doc, coda_token=conf.coda_token,
              conf_path=f'{conf.data_path}/coda_conf')


if __name__ == '__main__':
    doc.update_structure()
