import liff from "@line/liff"

export function initializeLiff(liffId) {
  this.liff
    .init({
      liffId: liffId
    })
    .then(() => {
      // start to use LIFF's api
      const OS = this.liff.getOS()
      if (OS === "web" && liff.isLoggedIn() === false){
        this.liff.login()
        this.initializeLiff(liffId)
      }else{
        if (this.liff.isLoggedIn() === true){
          return {"idToken": this.liff.getIDToken(), "os": OS, "status": "ok"}
        }else{
          return {"idToken": null, "os": OS, "status": "error"}
        }
      }
    })
    .catch((err) => {
      return {"idToken": null, "os": null, "status": err.message}
    })
}


export function get_bookmeta(idToken, uri, columnNames){
  fetch(`/api/${uri}?idToken=${idToken}`)
    .then(res => res.json())
    .then(
      (res) => {
        const timestamps = Array.from(res["items"].map(x => new Date(x["timestamp"]*1000).toLocaleDateString()))
        const rows = res["items"].map(item => columnNames.map(key => item["bookmeta"][key]))

        return {"timestamps": timestamps.reverse(), "bookmetas": rows.reverse(), "status": "ok"}

      })
    .catch(
      (err) => {
        this.liff.logout()
        return {"timestamp": null, "bookmeta": null, "status": err.message}
      }
    )
}
