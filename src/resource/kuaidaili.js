function aw(TB, oo, qo) {
    var mo = "", no = "";
    if (qo == 234) {
        do {
            oo[qo] = (-oo[qo]) & 0xff;
            oo[qo] = (((oo[qo] >> 1) | ((oo[qo] << 7) & 0xff)) - 191) & 0xff;
        } while (--qo >= 2);
    } else if (qo == 240) {
        do {
            oo[qo] = (oo[qo] - oo[qo - 1]) & 0xff;
        } while (--qo >= 3);
        qo = 1;
        for (; ;) {
            if (qo > 240) break;
            oo[qo] = ((((((oo[qo] + 30) & 0xff) + 91) & 0xff) << 5) & 0xff) | (((((oo[qo] + 30) & 0xff) + 91) & 0xff) >> 3);
            qo++;
        }
    } else if (qo == 233) {
        qo = 233;
        do {
            oo[qo] = (oo[qo] - oo[qo - 1]) & 0xff;
        } while (--qo >= 3);
        qo = 1;
        for (; ;) {
            if (qo > 233) {
                break;
            }
            oo[qo] = ((((((oo[qo] + 103) & 0xff) + 9) & 0xff) << 2) & 0xff) | (((((oo[qo] + 103) & 0xff) + 9) & 0xff) >> 6);
            qo++;
        }
    }
    var po = "";
    for (qo = 1; qo < oo.length - 1; qo++) {
        if (qo % 7) {
            po += String.fromCharCode(oo[qo] ^ TB);
        }
    }
    return po;
}