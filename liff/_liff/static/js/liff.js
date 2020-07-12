const liffId = document.referrer? document.referrer.split("/")[3]: "1654371886-xorapzM6"
initializeLiff(liffId)

function initializeLiff(myLiffId) {
  liff
    .init({
      liffId: myLiffId
    })
    .then(() => {
      // start to use LIFF's api
      if (liff.getOS() === "web" && liff.isLoggedIn() === false){
        liff.login()
        //initializeLiff(myLiffId)
      }else{
        displayLiffData()
        if (liff.getOS() !== "web"){
          mobile()
        }
      }
      document.getElementById("liffAppContent").textContent = "success"
    })
    .catch((err) => {
      document.getElementById("liffAppContent").textContent = err.message
    })
}


function displayLiffData() {
  document.getElementById('browserLanguage').textContent = liff.getLanguage()
  document.getElementById('sdkVersion').textContent = liff.getVersion()
  document.getElementById('isInClient').textContent = liff.isInClient()
  document.getElementById('isLoggedIn').textContent = liff.isLoggedIn()
  document.getElementById('deviceOS').textContent = liff.getOS()
  document.getElementById('lineVersion').textContent = liff.getLineVersion()
}

function mobile(){
  document.getElementById('closeWindowButton').addEventListener('click', () => {
    if (!liff.isInClient()) {
      //sendAlertIfNotInClient()
    }else{
      liff.closeWindow()
    }
  })
}
