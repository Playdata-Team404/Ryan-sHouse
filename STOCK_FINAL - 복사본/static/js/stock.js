function get_stock() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("실시간 주식 데이터 저장 성공")
        }
    };
    xhttp.open("GET", "getstock");
    xhttp.send();
}

function stockchart() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var img_name = this.responseText
            document.getElementById("chart_view").innerHTML = '<img src="./' + img_name + '" width=570 height=310>'
        }
    };
    xhttp.open("POST", "stockchart");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "stock_name=" + document.getElementById("stock_name").value;
    console.log(query)
    xhttp.send(query);
    // alert(document.getElementById('stock_name').value)
}

function wordcloud() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var img_name = this.responseText
            document.getElementById("cloud_view").innerHTML = '<img src="./' + img_name + '" width=550 height=300>'
        }
    };
    xhttp.open("POST", "wordcloud");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "stock_name=" + document.getElementById("stock_name").value;
    console.log(query)
    xhttp.send(query);
}

function upbit() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            coin = this.responseText
            img_name = document.getElementById("coin_name").value
            document.getElementById("upbit2").style.display = 'block';
            document.getElementById("upbit").innerHTML = coin
            var tmpDate = new Date();
            document.getElementById("upbit2").innerHTML = '<img src="./static/img/' + img_name + '.png?' +tmpDate.getTime()+'" width=550 height=300>'
        }
    };
    xhttp.open("POST", "upbit");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "coin_name=" + document.getElementById("coin_name").value
        + "&day=" + document.getElementById("day").value;
    console.log(query)
    xhttp.send(query);
};


function upbit_graph() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            data = this.responseText;
            data = eval(data)
            drawChart(data)
        }
    };
    xhttp.open("POST", "upbit_graph");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "coin_name=" + document.getElementById("coin_name").value;
    console.log(query)
    xhttp.send(query);
};


desc_array = ["삼성전자", "SK하이닉스", "NAVER", "카카오", "삼성전자우", "삼성바이오로직스", "LG화학", '삼성SDI', '현대차', '셀트리온']
stock_check = {
    "삼성전자": 'samsung-electronics-co-ltd', "SK하이닉스": "sk-hynix-inc", "NAVER": 'nhn-corp', "카카오": "kakao-corp", "삼성전자우": "samsung-electronics-co-pref",
    "삼성바이오로직스": "samsung-biologics-co-ltd", "LG화학": "lg-chemicals", '삼성SDI': "samsung-sdi", '현대차': "hyundai-motor", '셀트리온': "celltrion-inc"
}


window.onload = function () {

    function onClick() {
        document.querySelector('.modal_wrap').style.display = 'block';
        document.querySelector('.black_bg').style.display = 'block';
        const xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {

                lettering = Math.floor(Math.random() * desc_array.length)
                document.getElementById("letters").innerHTML = desc_array[lettering]
                document.getElementById("logo").innerHTML = '<br><img src="../static/img/' + desc_array[lettering] + '.jpg" width=90%>'
                document.getElementById("buy").innerHTML = '<br>주식 확인하러 가기! >>> <a href="https://kr.investing.com/equities/' + stock_check[desc_array[lettering]] + '" ' + 'target="_blank">' + desc_array[lettering] + '</a>'

            }
        };
        xhttp.open("GET", "popup");
        xhttp.send();
    }

    function offClick() {
        document.querySelector('.modal_wrap').style.display = 'none';
        document.querySelector('.black_bg').style.display = 'none';
    }
    document.getElementById('modal_btn').addEventListener('click', onClick);
    document.querySelector('.modal_close').addEventListener('click', offClick);
};



