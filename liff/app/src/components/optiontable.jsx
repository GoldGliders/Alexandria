import React from "react"
import { initializeLiff } from "./liffInit"
import liff from "@line/liff"
import Checkbox from "@material-ui/core/Checkbox"
import Button from "@material-ui/core/Button"

class OptionTable extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      options: {},
      displayName: null,
      liffId: this.props.liffId,
      idToken: null,
      error: null,
      error_msg: null
    }
    this.getResource = this.getResource.bind(this)
    this.row = this.row.bind(this)
    this.sendOption = this.sendOption.bind(this)
  }

  componentDidMount(){
    initializeLiff(this.state.liffId, this.getResource)
  }

  getResource(resp){
    if (resp["status"] === "ok"){
      fetch(`/api/option?idToken=${resp["idToken"]}`)
        .then(res => res.json())
        .then((res) => {
          const options = res["items"]["options"]
          const displayName = res["items"]["displayName"]
          this.setState({
            idToken: resp["idToken"],
            options: options,
            displayName, displayName,
            error: false
          })
        })
        .catch(err => {
          this.setState({
            error: true,
            error_msg: err.message
          })
        })
    }
  }

  row(options, displayName, idToken){
    const keys = Object.keys(options)
    return (
      <div>
        {
          keys.map((key, num) => (
            <div key={num}>
              <Checkbox color="primary" className="selector" type="checkbox" defaultChecked={options[key]} name={key}/>
              {displayName[key]}
            </div>
          ))
        }
        <Button variant="contained" onClick={() => this.sendOption(idToken)}>Save</Button>
      </div>
    )
  }

  sendOption(idToken){
    const checkbox = Array.from(document.getElementsByClassName("selector"))
    let jsn = {}
    checkbox.map((box) => {
      jsn = Object.assign(jsn, {[box.name]: box.checked})
    })

    fetch(`/api/option`, {
        method: "PUT",
        body: JSON.stringify({
          items: jsn,
          idToken: idToken
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    })
      .then((res) => {
        location.reload()
      })
      .catch((err) => {
        alert(`FAIL ${err.error_msg}`)
      })
  }

  render(){
    if (this.state.error){
      liff.logout()
      return (
        <div>
          <h1>{this.state.error_msg}</h1>
        </div>
      )
    }else{
      return (
        <div>
          {this.row(this.state.options, this.state.displayName, this.state.idToken)}
        </div>
      )
    }
  }
}

export default OptionTable
