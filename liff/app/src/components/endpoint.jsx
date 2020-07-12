import React from "react"
import liff from "@line/liff"

class Endpoint extends React.Component{
  constructor(props){
    super(props)
    this.state = ({
      liffId: this.props.liffId
    })
    this.initializeLiff = this.initializeLiff.bind(this)
  }

  componentDidMount(){
    this.initializeLiff()
  }

  initializeLiff(){
    liff
      .init({
        liffId: this.state.liffId
      })
      .then(() => {
        // start to use LIFF's api
        const OS = liff.getOS()
        if (OS === "web" && liff.isLoggedIn() === false){
          liff.login()
          this.initializeLiff()
        }else{
          if (liff.isLoggedIn() === true){
            this.setState({
              "idToken": liff.getIDToken(),
              "os": OS,
              "status": "ok"
            })
          }else{
            this.setState({
              "idToken": null,
              "os": OS,
              "status": "error"
            })
          }
        }
      })
      .catch((err) => {
        this.setState({
          "idToken": null,
          "os": null,
          "status": err.message
        })
      })
  }

  render(){
    return (
      <div>
      </div>
    )
  }
}

export default Endpoint
