import React from "react"
import { initializeLiff } from "./liffInit"
import liff from "@line/liff"
import Button from "@material-ui/core/Button"
import Card from "@material-ui/core/Card"
import CardActions from "@material-ui/core/CardActions"
import CardContent from "@material-ui/core/CardContent"
import Grid from "@material-ui/core/Grid"
import Typography from "@material-ui/core/Typography"
import { withStyles } from "@material-ui/core/styles"
import FavoriteBorderIcon from '@material-ui/icons/FavoriteBorder'
import FavoriteIcon from '@material-ui/icons/Favorite'
import { pink, grey } from '@material-ui/core/colors'

const useStyles = ((theme) => ({
  root: {
    flexGrow: 1,
  },
  card: {
    margin: 16,
    padding: 16,
  },
  innertext: {
    textAlign: "left",
    width: 220,
  },
  innercard: {
    margin: 4,
    height: 75,
    width: 300,
    padding: 0,
  },
  areaRow: {
    textAlign: "center",
  },
  text: {
    textAlign: "center",
  },
  textarea: {
  },
  button: {
    margin: 8,
  },
  librarybutton: {
    position: "absolute",
    padding: 0,
    marginLeft: "220px !important",
  },
  row: {
    textAlign: "left",
  },
  switches: {
    alignItems: "center",
  }
}))

class LibrarySelect extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      liffId: this.props.liffId,
      scopeField: ["北海道","東北","関東","中部","近畿", "中国", "四国","九州・沖縄"],
      selectedField: "地域",
      selectedArea: null,
      selectedPref: null,
      selectedCity: null,
      selectedLibrary: null,
      libraryColumns: ["formal"],
      url: "/api/onelibrary",
      level: 0,
      scope: "",
      libids: null,
      error: false,
      error_msg: null
    }
    this.getResource = this.getResource.bind(this)
    this.getScope = this.getScope.bind(this)
    this.putLibrary = this.putLibrary.bind(this)
    this.removeResourse = this.removeResourse.bind(this)
    this.scopeButton = this.scopeButton.bind(this)
    this.libraryTable = this.libraryTable.bind(this)
    this.scopeTable = this.scopeTable.bind(this)
    //this.registerTable = this.registerTable.bind(this)
  }

  componentDidMount(){
    initializeLiff(this.state.liffId, this.getResource)
  }

  getResource(resp){
    if (resp["status"] === "ok"){
      fetch(`/api/library?idToken=${resp["idToken"]}`)
        .then(res => res.json())
        .then((res) => {
          const rows = res["items"].map(item => item["libid"])
          this.setState({
            libids: rows,
            idToken: resp["idToken"]
          })
        })
        .catch((err) => {
          this.setState({
            error: true,
            error_msg: err.message
          })
        })
    }
  }

  getScope(fieldValue, url, level){
    //level = level === 3? level: level + 1
    level = level + 1
    let fieldName = ""
    switch (level){
      case 1:
        fieldName = "?area"
        break

      case 2:
        fieldName = "&pref"
        break

      case 3:
        fieldName = "&city"
        break

      default:
        break
    }

    url = url + `${fieldName}=${fieldValue}`
    const scope = `${this.state.scope}${fieldValue}>`
    fetch(`${url}&level=${level}`)
      .then(res => res.json())
      .then((res) => {
        let response = {}
        switch (level){
          case 1:
            response = {selectedArea: fieldValue}
            break

          case 2:
            response = {selectedPref: fieldValue}
            break

          case 3:
            response = {selectedCity: fieldValue}
            break

          default:
            break
        }

        this.setState(
          Object.assign(
            response,
            {scopeField: res["items"], selectedField: fieldValue, url: url, level: level, error: false, scope: scope}
          )
        )
      })
      .catch((err) => {
        this.setState({error: true, error_msg: err.message})
      }
    )
  }

  putLibrary(libid, idToken, formal, level){
    console.log(libid, idToken)
    fetch("/api/library", {
      method: "PUT",
      body: JSON.stringify({
        libid: libid,
        idToken: idToken
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
      .then(res => res.json())
      .then((res) => {
       if (res.status === 200){
         const libids = this.state.libids.concat([libid])
          this.setState({
            selectedLibrary: libid,
            libids: libids,
          })
        }else{
          this.setState({
            error: true,
            error_msg: res.message
          })
          alert(`FAIL ${res.message}`)
        }
      })
      .catch((err) => {
        this.setState({
          error: true,
          error_msg: err.message
        })
        alert(`FAIL ${err.message}`)
      })
  }

  scopeButton(classes){
    const table = this.state.scopeField.map((fieldValue, num) => (
      <Grid item xs={6} key={num} className={classes.areaRow}>
        <Button variant="contained" color="primary" onClick={() => {
          this.getScope(fieldValue, this.state.url, this.state.level)
        }} className={classes.button}>
          {fieldValue}
        </Button>
      </Grid>
    ))
    return (
      <Grid container justify="center">
        {table}
      </Grid>
    )
  }


  removeResourse(resourceName, targetName, targetId, idToken){
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
      .then((res) => {
        if (res.status === 204){
          this.setState({libids: this.state.libids.filter(item => item !== targetId)})
        }else{
          alert(`FAIL ${res.message}`)
        }
      })
      .catch((err) => {
        alert(`FAIL ${err.message}`)
      })
  }

  libraryTable = (classes) => {
    const rows = this.state.scopeField.map((fieldValue, rowNum) => {
      const formal = fieldValue["formal"]
      const libid = fieldValue["libid"]

      return (
        <Grid container justify="center" alignItems="center" item xs={12} sm={6} md={4} lg={3} className={classes.areaRow} key={rowNum} zeroMinWidth>
          <Card variant="outlined" className={classes.innercard}>
            <CardActions>
              <CardContent className={classes.textarea}>
                <Typography color="textPrimary" variant="body1" component="h2" className={classes.innertext}>
                  {formal}
                </Typography>
              </CardContent>
              <CardActions className={classes.librarybutton}>
                <Button onClick={() => {
                  this.state.libids.includes(libid)?
                    this.removeResourse("library", "", libid, this.state.idToken):
                    this.putLibrary(fieldValue["libid"], liff.getIDToken(), fieldValue["formal"], this.state.level)
                }}>
                  {
                    this.state.libids.includes(libid)?
                      <FavoriteIcon style={{fill: pink[400]}} />:
                      <FavoriteBorderIcon style={{fill: grey[400]}} />
                  }
                </Button>
              </CardActions>
            </CardActions>
          </Card>
        </Grid>
      )})

    return (
      <div>
        <Grid container justify="center">
          <Grid item xs={12} sm={4}>
            <Typography color="textPrimary" variant="h6" component="h1" className={classes.text}>
              {this.state.level === 0? this.state.selectedField: this.state.scope}
            </Typography>
          </Grid>
          <Grid container justify="center">
            {rows}
          </Grid>
        </Grid>
      </div>
    )
  }

  scopeTable = (classes) => {
    return (
      <div>
        <Grid container>
          <Grid item xs={12} sm={4}>
            <Typography color="textPrimary" variant="h6" component="h1" className={classes.text}>
              {this.state.level === 0? this.state.selectedField: this.state.scope}
            </Typography>
          </Grid>
        </Grid>
        {this.scopeButton(classes)}
      </div>
    )
  }

  /*
  registerTable = (library) => {
    return (
      <div>
        <h1>Succeed in registering {library}</h1>
        <Button variant="contained" color="primary" onClick={() => {liff.closeWindow()}}>close</Button>
      </div>
    )
  }
   */

  render(){
    const {classes} = this.props
    if (this.state.error){
      liff.logout()
      return(
        <div>
          <h1>{this.state.error_msg}</h1>
        </div>
      )
    }else if (this.state.level >= 3){
      return this.libraryTable(classes)
    }else{
      return this.scopeTable(classes)
    }
  }
}

export default withStyles(useStyles, {withTheme: true})(LibrarySelect)
