#include "common.hpp"
#include "msg.hpp"

using namespace std;
#define MY_ENCODING_TYPE  (PKCS_7_ASN_ENCODING | X509_ASN_ENCODING)

char *hashAlg(char *pubKeyAlg) {
    if (0 == strcmp(pubKeyAlg, szOID_CP_GOST_R3410EL)) {
        return (char *)szOID_CP_GOST_R3411;
    }
    if (0 == strcmp(pubKeyAlg, szOID_CP_GOST_R3410_12_512)) {
        return (char *)szOID_CP_GOST_R3411_12_512;
    }
    return (char *)szOID_CP_GOST_R3411_12_256;
}

HCRYPTMSG CryptMsg::get_handle() throw (CSPException) {
    LOG("CryptMsg::get_handle()\n");
    if (hmsg) {
        return hmsg;
    }
    hmsg = CryptMsgOpenToDecode(MY_ENC_TYPE, 0, 0, cprov? cprov->hprov:0, NULL, NULL);
    if (!hmsg) {
        throw CSPException("CryptMsg.get_handle: Couldn't open message for decode");
    }
    if ( !CryptMsgUpdate(hmsg, data, data_length, TRUE) ) {
        throw CSPException("CCryptMsg.get_handle: couldn't update message");
    }
    return hmsg;
}

int CryptMsg::num_signers() throw(CSPException) {
    LOG("CryptMsg::num_signers()\n");
    if (data && data_length) {
        return CryptGetMessageSignerCount(MY_ENCODING_TYPE, data, data_length);
    } else {
        return 0;
    }
}

bool CryptMsg::verify(DWORD n) throw(CSPException)
{
    CRYPT_VERIFY_MESSAGE_PARA VerifyParams;
    DWORD res, msg_size = 0;
    LOG("CryptMsg::verify(%lu)\n", n);

    // Initialize the VerifyParams data structure.
    ZeroMemory(&VerifyParams, sizeof(VerifyParams));
    VerifyParams.cbSize = sizeof(CRYPT_VERIFY_MESSAGE_PARA);
    VerifyParams.dwMsgAndCertEncodingType = MY_ENCODING_TYPE;
    if (cprov) {
        VerifyParams.hCryptProv = cprov->hprov;
    }

    res = CryptVerifyMessageSignature(
              &VerifyParams,
              n,
              data,
              data_length,
              NULL,
              &msg_size,
              NULL);
    LOG("    verification result: %lu, %lu\n", n, msg_size);
    return res && msg_size;
}

void CryptMsg::init(Crypt *ctx) throw(CSPException)
{
    cprov = ctx;
    data = NULL;
    data_length = 0;
    hmsg = 0;
    if (ctx) {
        ctx->ref();
    }
    LOG("    initialized msg: %p\n", this);

}

CryptMsg::CryptMsg(BYTE *STRING, DWORD LENGTH, Crypt *ctx, DWORD chunk_size) throw(CSPException)
{
    LOG("CryptMsg::CryptMsg(%p, %lu, %p)\n", STRING, LENGTH, ctx);
    init(ctx);
    data = new BYTE[LENGTH];
    data_length = LENGTH;
    data_chunk_size = chunk_size;
    memcpy(data, STRING, LENGTH);
};

CryptMsg::CryptMsg(Crypt *ctx, DWORD chunk_size) throw(CSPException)
{
    LOG("CryptMsg::CryptMsg(%p)\n", ctx);
    init(ctx);
    data_chunk_size = chunk_size;
}

void CryptMsg::add_recipient(Cert *c) throw(CSPException)
{
    LOG("CryptMsg::add_recipient(%p)\n", c);
    if (c) {
        c->ref();
        recipients.push_back(c);
    }
}

void CryptMsg::encrypt_data(BYTE *STRING, DWORD LENGTH, BYTE **s, DWORD *slen) throw(CSPException)
{
    LOG("CryptMsg::encrypt_data(%p, %u)\n", STRING, LENGTH);
    CRYPT_ALGORITHM_IDENTIFIER EncryptAlgorithm;
    CRYPT_ENCRYPT_MESSAGE_PARA EncryptParams;
    DWORD nrecs = recipients.size();
    LOG("    nrecs: %i\n", nrecs);
    PCCERT_CONTEXT *pRecipientCert = new PCCERT_CONTEXT[nrecs];
    vector<Cert *>::const_iterator cii;
    int i = 0;
    for(cii=recipients.begin(); cii!=recipients.end(); cii++) {
        LOG("    adding recipient cert %p\n", (*cii)->pcert);
        pRecipientCert[i++] = (*cii)->pcert;
    }
    LOG("    processed all recipient certs\n");

    // Инициализация структуры с нулем.
    memset(&EncryptAlgorithm, 0, sizeof(CRYPT_ALGORITHM_IDENTIFIER));
//     EncryptAlgorithm.pszObjId = OID_CipherVar_Default;
    EncryptAlgorithm.pszObjId = (LPSTR)ENCRYPT_OID;

    // Инициализация структуры CRYPT_ENCRYPT_MESSAGE_PARA.
    memset(&EncryptParams, 0, sizeof(EncryptParams));
    EncryptParams.cbSize =  sizeof(EncryptParams);
    EncryptParams.dwMsgEncodingType = MY_ENCODING_TYPE;
    if (cprov) {
        EncryptParams.hCryptProv = cprov->hprov;
    }
    EncryptParams.ContentEncryptionAlgorithm = EncryptAlgorithm;

    LOG("    getting encrypted data size\n");
    // Вызов функции CryptEncryptMessage.
    if(!CryptEncryptMessage(
                &EncryptParams,
                nrecs,
                pRecipientCert,
                STRING,
                LENGTH,
                NULL,
                slen)) {
        DWORD err = GetLastError();
        LOG("    error getting encrypted data size %x\n", err);
        delete[] pRecipientCert;
        throw CSPException("CryptMsg.encrypt_data: Getting EncrypBlob size failed.", err);
    }
    LOG("    encrypted data size is %u\n", *slen);
    // Распределение памяти под возвращаемый BLOB.
    *s = (BYTE*)malloc(*slen);

    if(!*s) {
        DWORD err = GetLastError();
        delete[] pRecipientCert;
        throw CSPException("CryptMsg.encrypt_data: Memory allocation error while encrypting.", err);
    }

    LOG("    encrypting data\n");
    // Повторный вызов функции CryptEncryptMessage для зашифрования содержимого.
    if(!CryptEncryptMessage(
                &EncryptParams,
                nrecs,
                pRecipientCert,
                STRING,
                LENGTH,
                *s,
                slen)) {
        DWORD err = GetLastError();
        LOG("    encryption error %x\n", err);
        delete[] pRecipientCert;
        free((void *)*s);
        throw CSPException("CryptMsg.encrypt_data: Encryption failed.", err);
    }
    LOG("    encrypted succesfully\n");
    delete[] pRecipientCert;
}

void CryptMsg::decrypt_by_cert(Cert *crt) throw(CSPException, CSPNotFound)
{
    HCRYPTPROV hprov;
    DWORD dwKeySpec;

    if(!( CryptAcquireCertificatePrivateKey(
        crt->pcert,
        0,
        NULL,
        &hprov,
        &dwKeySpec,
        NULL)))
    {
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.decrypt_by_cert: couldn't acquire cert private key", err);
    }
    HCRYPTMSG hmsg = get_handle();
    DWORD recipient_idx = 0;
    DWORD num_recipients = 0;
    DWORD temp = sizeof(DWORD);
    PCERT_INFO pci = NULL;

    if (!CryptMsgGetParam(hmsg, CMSG_RECIPIENT_COUNT_PARAM, 0, &num_recipients, &temp)) {
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.decrypt_by_cert: couldn't get recipient count", err);
    }

    for (recipient_idx = 0; recipient_idx < num_recipients; recipient_idx++)
    {
        temp = 0;
        if (pci) {
            free(pci);
            pci = NULL;
        }
        if (!CryptMsgGetParam(hmsg, CMSG_RECIPIENT_INFO_PARAM, recipient_idx, NULL, &temp)) {
            DWORD err = GetLastError();
            throw CSPException("CryptMsg.decrypt_by_cert: couldn't get recipient info size", err);
        }
        pci = (PCERT_INFO) malloc(temp);
        if (!CryptMsgGetParam(hmsg, CMSG_RECIPIENT_INFO_PARAM, recipient_idx, pci, &temp)) {
            if (pci) {
                free(pci);
            }
            DWORD err = GetLastError();
            throw CSPException("CryptMsg.decrypt_by_cert: couldn't get recipient info data", err);
        }
        if (CertCompareCertificate(MY_ENCODING_TYPE, pci, crt->pcert->pCertInfo)) {
            break;
        }
    }
    if (pci) {
        free(pci);
    }
    if (recipient_idx >= num_recipients) {
        throw CSPNotFound("CryptMsg.decrypt_by_cert: cert not found in recipient infos", 0);
    }

    CMSG_CTRL_DECRYPT_PARA decr_para;
    ZeroMemory(&decr_para, sizeof(decr_para));
    decr_para.cbSize = sizeof(decr_para);
    decr_para.hCryptProv = hprov;
    decr_para.dwKeySpec = dwKeySpec;
    decr_para.dwRecipientIndex = recipient_idx;

    if (!CryptMsgControl(hmsg, 0, CMSG_CTRL_DECRYPT, &decr_para)) {
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.decrypt_by_cert: decrypt failed", err);
    }

    if (!CryptReleaseContext(hprov, 0)) {
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.decrypt_by_cert: couldn't release private key", err);
    }
}

void CryptMsg::decrypt(BYTE **s, DWORD *slen, CertStore *store) throw(CSPException, CSPNotFound)
{
    CRYPT_DECRYPT_MESSAGE_PARA  decryptParams;
    //   Инициализация структуры CRYPT_DECRYPT_MESSAGE_PARA.
    memset(&decryptParams, 0, sizeof(CRYPT_DECRYPT_MESSAGE_PARA));
    decryptParams.cbSize = sizeof(CRYPT_DECRYPT_MESSAGE_PARA);
    decryptParams.dwMsgAndCertEncodingType = MY_ENCODING_TYPE;
    decryptParams.cCertStore = 1;
    decryptParams.rghCertStore = &store->hstore;

    //  Расшифрование сообщения

    //  Вызов фнукции CryptDecryptMessage для получения возвращаемого размера данных.
    if(!CryptDecryptMessage(
                &decryptParams,
                data,
                data_length,
                NULL,
                slen,
                NULL)) {
        DWORD err = GetLastError();
        switch (err) {
            case CRYPT_E_NO_DECRYPT_CERT:
                throw CSPNotFound( "CryptMsg.decrypt: No certificate for decryption", err);
            default:
                throw CSPException( "CryptMsg.decrypt: Error getting decrypted message size", err);
        }
    }

    // Выделение памяти под возвращаемые расшифрованные данные.
    *s = (BYTE*)malloc(*slen);
    if(!*s) {
        DWORD err = GetLastError();
        throw CSPException( "Memory allocation error while decrypting", err);
    }
    // Вызов функции CryptDecryptMessage для расшифрования данных.
    if(!CryptDecryptMessage(
                &decryptParams,
                data,
                data_length,
                *s,
                slen,
                NULL)) {
        DWORD err = GetLastError();
        free((void *)*s);
        throw CSPException( "Error decrypting the message", err);
    }
}

//void CryptMsg::add_signer(Cert *c) throw(CSPException)
//{
    //if (c) {
        //c->ref();
        //signers.push_back(c);
    //}
//}

bool CryptMsg::verify_cert(Cert *c) throw(CSPException)
{
    HCRYPTMSG hmsg = get_handle();
    return CryptMsgControl(hmsg, 0, CMSG_CTRL_VERIFY_SIGNATURE, c->pcert->pCertInfo);
}

DWORD CryptMsg::get_type() throw(CSPException)
{
    DWORD type = 0, temp = sizeof(DWORD);
    HCRYPTMSG hmsg = get_handle();
    if (!CryptMsgGetParam(hmsg, CMSG_TYPE_PARAM, 0, &type, &temp)) {
        throw CSPException("CryptMsg.get_type: Couldn't get message type");
    }
    return type;
}

void CryptMsg::get_data(BYTE **s, DWORD *slen) throw(CSPException)
{
    HCRYPTMSG hmsg = get_handle();
    if(!CryptMsgGetParam(
                hmsg,                      /* Handle to the message*/
                CMSG_CONTENT_PARAM,        /* Parameter type*/
                0,                         /* Index*/
                NULL,             /* Pointer to the blob*/
                slen)) {
        /* Size of the blob*/
        throw CSPException("CryptMsg.get_data: Couldn't get decoded data size");
    }
    *s = (BYTE *) malloc(*slen);
    if(!CryptMsgGetParam(
                hmsg,                      /* Handle to the message*/
                CMSG_CONTENT_PARAM,        /* Parameter type*/
                0,                         /* Index*/
                *s,             /* Pointer to the blob*/
                slen)) {
        /* Size of the blob*/
        free((void *)*s);
        throw CSPException("CryptMsg.get_data: Couldn't get decoded data");
    }
}

void CryptMsg::sign_data(BYTE *STRING, DWORD LENGTH, BYTE **s, DWORD *slen, Cert *signer, bool detach) throw(CSPException)
{
    LOG("CryptMsg::sign_data(%p, %u, %p, %i)\n", STRING, LENGTH, signer, detach);
    CRYPT_SIGN_MESSAGE_PARA  SigParams;
    ZeroMemory(&SigParams, sizeof(SigParams));
    PCCERT_CONTEXT pCert = signer->pcert;

    const BYTE* DataArray[] = { STRING };
    DWORD SizeArray[] = { LENGTH };

    // Initialize the signature structure.
    SigParams.cbSize = sizeof(CRYPT_SIGN_MESSAGE_PARA);
    SigParams.dwMsgEncodingType = MY_ENCODING_TYPE;
    SigParams.pSigningCert = pCert;
    //SigParams.HashAlgorithm.pszObjId = szOID_RSA_SHA1RSA;
    SigParams.HashAlgorithm.pszObjId = hashAlg(pCert->pCertInfo->SubjectPublicKeyInfo.Algorithm.pszObjId);
    SigParams.HashAlgorithm.Parameters.cbData = 0;
    SigParams.cMsgCert = 1;
    SigParams.rgpMsgCert = &pCert;
    LOG("1\n");

    // First, get the size of the signed BLOB.
    if(!CryptSignMessage(
                &SigParams,
                detach,
                1,
                DataArray,
                SizeArray,
                NULL,
                slen)) {
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.sign_data: Getting signed BLOB size failed", err);
    }
    LOG("2 %u\n", *slen);

    // Allocate memory for the signed BLOB.
    *s = (BYTE *)malloc(*slen);
    LOG("2a\n");
    if(!*s) {
        LOG("2b\n");
        DWORD err = GetLastError();
        LOG("2c\n");
        throw CSPException("CryptMsg.sign_data: Memory allocation error while signing", err);
    }
    LOG("3\n");

    // Get the signed message BLOB.
    if(!CryptSignMessage(
                &SigParams,
                detach,
                1,
                DataArray,
                SizeArray,
                *s,
                slen)) {
        DWORD err = GetLastError();
        free((void *)*s);
        throw CSPException("CryptMsg.sign_data: Error getting signed BLOB", err);
    }
    LOG("4\n");
}

CryptMsg::~CryptMsg() throw(CSPException)
{
    LOG("CryptMsg::~CryptMsg(%p)\n", this);
    vector<Cert *>::const_iterator cii;
    //for(cii=signers.begin(); cii!=signers.end(); cii++) {
        //if (*cii)
            //(*cii)->unref();
    //}
    for(cii=recipients.begin(); cii!=recipients.end(); cii++) {
        if (*cii)
            (*cii)->unref();
    }
    if (cprov) {
        cprov->unref();
    }
    if (data) {
        delete[] data;
    }
    if (hmsg && !CryptMsgClose(hmsg)) {
        throw CSPException("~CryptMsg: Couldn't close message");
    }

};

BOOL WINAPI msgStreamCallback (
    const void *pvArg,
    BYTE *pbData,
    DWORD cbData,
    BOOL fFinal) {

    std::vector<unsigned char> *buf = (std::vector<unsigned char>*)pvArg;
    buf->insert(buf->end(), pbData, pbData + cbData);
    return TRUE;
}


void CryptMsg::encrypt_streaming(BYTE **s, DWORD *slen) throw(CSPException)
{
    LOG("CryptMsg::encrypt_data_streaming()\n");
    CRYPT_ALGORITHM_IDENTIFIER EncryptAlgorithm;
    memset(&EncryptAlgorithm, 0, sizeof(CRYPT_ALGORITHM_IDENTIFIER));
    EncryptAlgorithm.pszObjId = (LPSTR)ENCRYPT_OID;

    DWORD nrecs = recipients.size();
    LOG("    nrecs: %i\n", nrecs);

	CMSG_ENVELOPED_ENCODE_INFO ei;
	memset(&ei, 0, sizeof(CMSG_ENVELOPED_ENCODE_INFO));
	ei.cbSize = sizeof(CMSG_ENVELOPED_ENCODE_INFO);
    if (cprov) {
        ei.hCryptProv = cprov->hprov;
    }
	ei.ContentEncryptionAlgorithm = EncryptAlgorithm;
	ei.pvEncryptionAuxInfo = NULL;
	ei.cRecipients = nrecs;
	ei.rgpRecipients = new PCERT_INFO[nrecs];
    int i = 0;
    vector<Cert *>::const_iterator cii;
    for(cii=recipients.begin(); cii!=recipients.end(); cii++) {
        LOG("    adding recipient cert %p\n", (*cii)->pcert);
        ei.rgpRecipients[i++] = (*cii)->pcert->pCertInfo;
    }
    LOG("    processed all recipient certs\n");

    std::vector<unsigned char> buf;
	CMSG_STREAM_INFO si = {};
	si.cbContent = CMSG_INDEFINITE_LENGTH;
	si.pfnStreamOutput = msgStreamCallback;
	si.pvArg = &buf;

    HCRYPTMSG hmsg = CryptMsgOpenToEncode(
		MY_ENC_TYPE,                 // encoding type
		0,                             // flags
		CMSG_ENVELOPED,              // message type
		&ei, // pointer to structure
		NULL,                           // inner content OID
		&si                            // stream information
	);
    if (!hmsg) {
        delete[] ei.rgpRecipients;
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.encrypt_data_streaming: CryptMsgOpenToEncode failed.", err);
    }
    LOG("   opened message to encrypt\n");
    DWORD processed_bytes = 0;
    DWORD chunk_size = 0;
    for (BYTE *dataptr = data; processed_bytes < data_length; dataptr += data_chunk_size) {
        chunk_size = data_chunk_size;
        BOOL final_chunk = FALSE;
        if (processed_bytes + chunk_size > data_length) {
            chunk_size = data_length - processed_bytes;
            final_chunk = TRUE;
        }
        if ( !CryptMsgUpdate(hmsg, dataptr, chunk_size, final_chunk) ) {
            delete[] ei.rgpRecipients;
            throw CSPException("CCryptMsg.encrypt_data_streaming: couldn't update message");
        }
        processed_bytes += chunk_size;
    }
    LOG("   updated message\n");
    if (!CryptMsgClose(hmsg)) {
        delete[] ei.rgpRecipients;
        throw CSPException("CCryptMsg.encrypt_data_streaming: couldn't close message");
    }
    *slen = buf.size();
    *s = (BYTE *) malloc(*slen);
    memcpy(*s, buf.data(), *slen);
    LOG("   got message data\n");
    delete[] ei.rgpRecipients;
}

void CryptMsg::sign_data_streaming(BYTE *STRING, DWORD LENGTH, BYTE **s, DWORD *slen, Cert *signer, bool detach) throw(CSPException)
{
    LOG("CryptMsg::sign_data_streaming(%p, %u, %p, %i)\n", STRING, LENGTH, signer, detach);
    PCCERT_CONTEXT pCert = signer->pcert;
    const BYTE* DataArray[] = { STRING };
    DWORD SizeArray[] = { LENGTH };

	CMSG_SIGNED_ENCODE_INFO ei = {};
	ei.cbSize = sizeof(CMSG_SIGNED_ENCODE_INFO);

    int cSigners = 1;
	ei.cSigners = cSigners;
	ei.rgSigners = new CMSG_SIGNER_ENCODE_INFO[cSigners]();

	ei.cCertEncoded = cSigners;
	ei.rgCertEncoded =  new CERT_BLOB[cSigners]();

	ei.rgSigners[0].cbSize = sizeof(CMSG_SIGNER_ENCODE_INFO);
	ei.rgSigners[0].pCertInfo = pCert->pCertInfo;

    std::vector<unsigned char> buf;
	CMSG_STREAM_INFO si = {};
	si.cbContent = CMSG_INDEFINITE_LENGTH;
	si.pfnStreamOutput = msgStreamCallback;
	si.pvArg = &buf;

    HCRYPTPROV signerHprov;
    DWORD dwKeySpec;
    DWORD flags = 0;
    if (detach) {
        flags = CMSG_DETACHED_FLAG;
    }

    if(!( CryptAcquireCertificatePrivateKey(
        pCert,
        0,
        NULL,
        &signerHprov,
        &dwKeySpec,
        NULL)))
    {
        delete[] ei.rgCertEncoded;
        delete[] ei.rgSigners;
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.sign_data_streaming: couldn't acquire cert private key", err);
    }
    ei.rgSigners[0].hCryptProv = signerHprov;
    ei.rgSigners[0].dwKeySpec = dwKeySpec;
	ei.rgSigners[0].HashAlgorithm.pszObjId = hashAlg(pCert->pCertInfo->SubjectPublicKeyInfo.Algorithm.pszObjId);
	ei.rgSigners[0].pvHashAuxInfo = NULL;
	ei.rgCertEncoded[0].cbData = pCert->cbCertEncoded;
	ei.rgCertEncoded[0].pbData = pCert->pbCertEncoded;

    HCRYPTMSG hmsg = CryptMsgOpenToEncode(
		MY_ENC_TYPE,                 // encoding type
		flags,                             // flags
		CMSG_SIGNED,              // message type
		&ei, // pointer to structure
		NULL,                           // inner content OID
        &si
	);
    if (!hmsg) {
        delete[] ei.rgCertEncoded;
        delete[] ei.rgSigners;
        DWORD err = GetLastError();
        throw CSPException("CryptMsg.sign_data_streaming: CryptMsgOpenToEncode failed.", err);
    }
    LOG("   opened message to encrypt\n");

    DWORD processed_bytes = 0;
    DWORD chunk_size = 0;
    for (BYTE *dataptr = STRING; processed_bytes < LENGTH; dataptr += data_chunk_size) {
        chunk_size = data_chunk_size;
        BOOL final_chunk = FALSE;
        if (processed_bytes + chunk_size > LENGTH) {
            chunk_size = LENGTH - processed_bytes;
            final_chunk = TRUE;
        }
        if ( !CryptMsgUpdate(hmsg, dataptr, chunk_size, final_chunk) ) {
            delete[] ei.rgCertEncoded;
            delete[] ei.rgSigners;
            throw CSPException("CCryptMsg.sign_data_streaming: couldn't update message");
        }
        processed_bytes += chunk_size;
    }

    if (!CryptMsgClose(hmsg)) {
        delete[] ei.rgCertEncoded;
        delete[] ei.rgSigners;
        throw CSPException("CCryptMsg.sign_data_streaming: couldn't close message");
    }
    *slen = buf.size();
    *s = (BYTE *) malloc(*slen);
    memcpy(*s, buf.data(), *slen);
    LOG("   got message data\n");
    delete[] ei.rgCertEncoded;
    delete[] ei.rgSigners;
}
