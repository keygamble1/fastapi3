import { writable } from "svelte/store";


const persist_storage=(key,initValue)=>{
    const storedValuestr=localStorage.getItem(key)
    // localsorage 이걸로 가져오는건 항상 문자열임
    //  이 문자열을 javascript화 시켜야 int든 뭐든 다 변환가능
    // 이때 변환한 javascript를 subscribe에 넣어서 검증
    // 후에다시 json형태바꿈
    // localdtorage에 자동으로 등록된다고보면됨 
    // localstorage로 getitem (key)를 받으면 json형태가되는데 이걸 javascript화시킴 
    // javascirpt화시킨후에 콜백함수 호출 set item후 json으로 다시 변경

    // 이건현재 key값받은 json형태임
    const store=writable(storedValuestr != null ? JSON.parse(storedValuestr) : initValue)
    // json.parse= json->javascript형태로
    // json.parse javascript화
    // json.stringfy= javascript->json형태로
    // json으로 변경 false시 0
    store.subscribe((val)=>{
        
        localStorage.setItem(key,JSON.stringify(val))
        // json형식의 문자열로되는거
    })
    // localstroage는 클라의 저장소일뿐 api로하려면 params에 직접넣어야함
    
    return store
}
export const page=persist_storage("page",0)
export const access_token=persist_storage("access_token","")
export const username=persist_storage("username","")
export const is_login=persist_storage("is_login",false)
export const keyword=persist_storage("keyword","")
        // 콜백을 호출하는함수 subscribe가먼저시행되고나서 val이게 실햄됨
        // store.subscribe, setTimeout, Array.forEach 등등 콜백함수를 실행하는 함수가있따
        // , Promise, EventListener, setInterval(), fetch, process.nextTick()
        // Promise fetch로 콜백함수를 실행하는 함수, EventLister Array.foreach등등도 그럼 
        // store.subscribe 호출 즉 변경될때마다 계속 실행된다
 
    // 그냥 함수쓰면 인스턴스 생성시마다 계속 바뀌는데
    // 얘는 한번정의시 this가 그대로 유지된다고보면됨 인스턴스 실행해도 
    // 한번 고정된 함수가 가져온 변수는 그대로 유지됨
    // 이렇게함으로써 콜백함수 씀
    // 외부에서 매개변수를 받고 쓴다
    // 이 외부는 다른파일이라고보면됨




// const page썼기때문에 다른곳에서도 page를 호출해야함 default는 맘대로 받을수있음

// 초깃값 0
// 쓰기가능한 page
// 새로고침을하면 초기화됨 이것만쓸시
