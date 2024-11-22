import qs from "qs"
import { push } from "svelte-spa-router"
import { get } from "svelte/store"
import { access_token, is_login } from "./store"
const fastapi=(operation,url,parmas,success_callback,failure_callback)=>{
    let method=operation
    let content_type='application/json'
    // option은 method와 headers가 있어야함 (제약조건)
// fetch("/api",{method:post,headers:{contenttype,body:json.stringfy}})
    let body=JSON.stringify(parmas)
    if(operation==='login'){
        method='post'
        content_type='application/x-www-form-urlencoded'
        body=qs.stringify(parmas)
        // qs=application/x-www-form-urlencoded타입으로 변경하는 함수임
    }
    let _url=import.meta.env.VITE_SERVER_URL +url
    // 파라미터 조립
    if(method==='get'){
        _url += '?' +new URLSearchParams(parmas)
    }
    let options={
        // method headrs body로 구성된다보자
        method:method,
        headers:{
            "Content-type":content_type
        }

    }
    const _access_token=get(access_token)
    if (_access_token){
        options.headers["Authorization"] = "Bearer "+_access_token
    }
    if(method!=='get'){
        options['body']=body
        // body안에 json으로 된걸 다 넣는거
    }
    // then이나 catch가 나오기전에는 프로미스형태고 그이후 then안에는 객체가있음
    // response=> 여기서 response는 객체임
    fetch(_url,options).then(
        // _url은 제쳐두고 options의 제약조건이 json이니까 urlsearchparams의 json이 
        // 제약조건으로인해 json만 response 프로미스에 들어간다고보자
        // urlseachParams의 키값과 값이 다 넣어진 _url이라고보자
        // then안으로들어온이상 프로미스가아닌 객체 해결되면 객체로 방환된다
                response=>{
                    if(response.status===204){
                        if(success_callback){
                            success_callback()
                        }
                        return
                        // post메서드라도 json을 돌려줄필요가없음
                    }
            response.json().then(
                json=>{
                    if(response.status>=200 && response.status <300){
                        if(success_callback){
                            success_callback(json)
                        }
                    }else if(operation !=='login' && response.status===401){
                        // 스토어변수 $못씀 api에서 가져와서 쓰는거기때문
                        access_token.set('')
                        username.set('')
                        is_login(false)
                        alert("로그인필요")
                        push('/user-login')
                    }
                    else{
                        if(failure_callback){
                            failure_callback(json)
                            // status바깥이면 뭐가 있는지 확이해봐야할듯?
                        }else{
                            alert(JSON.stringify(json))
                            // 그외에는 알아서 json으로 바꾸고
                        }
                    }
                }
            )
        }
    )
}
export default fastapi 
    // urlsearchparams는 name=a%age=1이렇게 되어있을때 name:a apge:1로 딕셔너리로바꾸는것
    // value[,replace[,space]]
    // 이런식으로됨  javascript값 객체 배열 숫자 =value
    // replacer=데이터필터링하거나 특정항목포함배열
    // spae=드여쓰기 설정
