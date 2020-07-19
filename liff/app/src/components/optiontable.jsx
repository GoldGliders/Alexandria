import React from "react"
import { initializeLiff } from "./liffInit"
import liff from "@line/liff"
import Checkbox from "@material-ui/core/Checkbox"
import Button from "@material-ui/core/Button"
import Card from "@material-ui/core/Card"
import CardActions from "@material-ui/core/CardActions"
import CardContent from "@material-ui/core/CardContent"
import CardMedia from "@material-ui/core/CardMedia"
import Grid from "@material-ui/core/Grid"
import Switch from "@material-ui/core/Switch"
import FormGroup from '@material-ui/core/FormGroup'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Typography from "@material-ui/core/Typography"
import { withStyles } from "@material-ui/core/styles"

const useStyles = ((theme) => ({
  root: {
    flexGrow: 1,
  },
  card: {
    margin: 16,
  },
  button: {
    marginTop: 16,
    marginBottom: 32,
  },
  row: {
    textAlign: "left",
  },
  switches: {
    alignItems: "center",
  }
}))

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

  row(options, displayName, idToken, classes){
    const keys = Object.keys(options)
    return (
      <div>
        <Grid container justify="center">
          <FormGroup>
            {
              keys.map((key, num) => (
                <FormControlLabel
                  control={
                    <Switch color="primary" className="selector" type="checkbox"
                      defaultChecked={options[key]} value="checked" name={key}
                      //onChange={this.handleChange}
                    />}
                  label={displayName[key]}
                  key={num}
                />
              ))
            }
          </FormGroup>
          <Grid container justify="center" className={classes.button} >
            <Button variant="contained" onClick={() => this.sendOption(idToken)}>Save</Button>
          </Grid>
        </Grid>
      </div>
    )
  }

  sendOption(idToken){
    const checkbox = Array.from(document.getElementsByClassName("MuiSwitch-input"))
    let options = {}
    checkbox.forEach((box) => {
      options[box.name] = box.checked
    })
    fetch(`/api/option`, {
        method: "PUT",
        body: JSON.stringify({
          items: options,
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
    const {classes} = this.props
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
          <Card variant="outlined" className={classes.card}>
            {this.row(this.state.options, this.state.displayName, this.state.idToken, classes)}
          </Card>
        </div>
      )
    }
  }
}

//export default OptionTable
export default withStyles(useStyles, {withTheme: true})(OptionTable)
