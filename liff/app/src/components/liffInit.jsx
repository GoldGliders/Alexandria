import liff from "@line/liff"

export function initializeLiff(liffId, func) {
  liff
    .init({
      liffId: liffId
    })
    .then(() => {
      // start to use LIFF's api
      const OS = liff.getOS()
      if (OS === "web" && liff.isLoggedIn() === false){
        liff.login()
        this.initializeLiff(liffId, func)
      }else{
        if (liff.isLoggedIn() === true){
          const resp = {"idToken": liff.getIDToken(), "os": OS, "status": "ok"}
          func(resp)
        }else{
          //resp = {"idToken": null, "os": OS, "status": "error"}
        }
      }
    })
    .catch((err) => {
      //resp = {"idToken": null, "os": null, "status": err.message}
    })
}

export function getBookmeta(idToken, uri, columnNames){
  console.log("hello")
  fetch(`/api/${uri}?idToken=${idToken}`)
    .then(res => res.json())
    .then((res) => {
        const timestamps = Array.from(res["items"].map(x => new Date(x["timestamp"]*1000).toLocaleDateString()))
        const rows = res["items"].map(item => columnNames.map(key => item["bookmeta"][key]))

        return {"timestamps": timestamps.reverse(), "bookmetas": rows.reverse(), "status": "ok"}

      })
    .catch((err) => {
      console.log(err.message)
        liff.logout()
        return {"timestamp": null, "bookmeta": null, "status": err.message}
      }
    )
}
