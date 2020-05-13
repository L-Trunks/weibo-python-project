//unicode转中文
function exchangeUnicode(str) {
//    str = JSON.stringify(str)
    str = str.replace(/(\\u)(\w{1,4})/gi, ($0) => {
        return (String.fromCharCode(parseInt((escape($0).replace(/(%5Cu)(\w{1,4})/g, "$2")),
            16)));
    });
//    str = JSON.parse(str);
    return str;
}