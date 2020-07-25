import React from "react"
import liff from "@line/liff"
import Button from "@material-ui/core/Button"
import { withStyles } from "@material-ui/core/styles"
import SearchIcon from '@material-ui/icons/Search'
import DeleteIcon from '@material-ui/icons/Delete'

const useStyles = ((theme) => ({
  button: {
    padding: 0,
  },
  icon: {
    fill: "black",
  }
}))

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
      idToken:  this.props.idToken,
      api_url:  this.props.api_url,
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
      fetch(`${this.state.api_url}/${resourceName}`, {
	mode: "cors",
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
        .then((res) => {
          if (res.status === 204){
            window.location.reload()
          }else{
            alert(`FAIL ${res.message}`)
          }
        })
        .catch((err) => {
            alert(`FAIL ${err.message}`)
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
    const {classes} = this.props
    return (
      <div>
        {
          this.state.funcName === "bookmark"? (
            <Button color="primary" className={classes.button} onClick={() => {this.multiFunc("history")}}>
              <SearchIcon className={classes.icon} />
            </Button>
          ): (
          null
          )
        }
        <Button color="primary" className={classes.button} onClick={() => {this.multiFunc(this.state.funcName)}}>
          {this.state.funcName === "history"?
            <SearchIcon className={classes.icon} />:
            <DeleteIcon className={classes.icon} />
          }
        </Button>
        </div>
    )
  }
}

//export default MultiButton
export default withStyles(useStyles, {withTheme: true})(MultiButton)
