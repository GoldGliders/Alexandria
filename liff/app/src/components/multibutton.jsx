import React from "react"
import liff from "@line/liff"

class MultiButton extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      funcName: this.props.funcName,
      text:     this.props.text,
      isbn:     this.props.isbn,
      title:    this.props.title,
      formal:   this.props.formal,
      libid:    this.props.libid,
      idToken:  this.props.idToken
    }
    this.sendIsbn = this.sendIsbn.bind(this)
    this.removeResourse = this.removeResourse.bind(this)
    this.multiFunc = this.multiFunc.bind(this)
  }

  sendIsbn(isbn) {
    liff.sendMessages([{
      type: "text",
      text: isbn
    }])
      .then(() => {
        liff.closeWindow()
      })
      .catch((err) => {
        this.setState({
          err: true,
          err_msg: err.message
        })
      })
  }

  removeResourse(resourceName, targetName, targetId, idToken){
    if (window.confirm(`Do you remove the ${resourceName} below?\n${targetName}`)){
      fetch(`/api/${resourceName}`, {
        method: "DELETE",
        body: JSON.stringify({
          targetId: targetId,
          idToken: idToken
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
        .then(res => res.json())
        .then(res => {
          if (res.status == 204){
            location.reload()
          }else{
            alert(`FAIL ${res.message}`)
          }
        })
        .catch(err => {
            alert(`FAIL ${res.message}`)
        })
    }
  }

  multiFunc(funcName){
    switch(funcName){
      case "history":
        this.sendIsbn(this.state.isbn)
        break

      case "bookmark":
        this.removeResourse(funcName, this.state.title, this.state.isbn, this.state.idToken)
        break

      case "library":
        this.removeResourse(funcName, this.state.formal, this.state.libid, this.state.idToken)
        break

      default:
        break
    }
  }

  render(){
    return (
      <button onClick={() => {
        this.multiFunc(this.state.funcName)
      }}>
        {this.state.text}
      </button>
    )
  }
}

export default MultiButton
