
//############Movement gait||运动步态
enum gait {
    //% block="Trot"
    3,
    //% block="F_TROT"
    4,
    //% block="S_TROT"
    5,
    //% block="Crawl"
    6
    
      
}

//############Actions||动作组
enum Choice{
    //% block="0"
    0
    //% block="1"
    1,
    //% block="2"
    2
    
}

//############Actions state||动作组状态
enum Actions{
    //% block="Enable"
    1,
    //% block="Not_Enable"
    0

}


 //############Movement direction||运动方向
enum Mov_dir{
    //% block="Forward"
    0,
    //% block="Backward"
    1,
    //% block="Turn_left"
    2,
    //% block="Turn_right"
    3,
    //% block="Shift_left"
    4,
    //% block="Shift_right"
    5
}

//############Movement Angle||运动角度
enum Mov_ang{
    //% block="Left_swing"
    0,
    //% block="Right_swing"
    1,
    //% block="Look_down"
    2,
    //% block="Look_up"
    3,
    //% block="Yaw_left"
    4,
    //% block="Yaw_right"
    5
}

// //############PWM||PWM
// enum PWM{
//     //% block="0"
//     0
//     //% block="1"
//     1,
//     //% block="2"
//     2,
//     //% block="3"
//     3
    
// }

//% color="#0fbc11" iconWidth=60 iconHeight=50
namespace Quadruped {
    //###Start||初始化
    //% block="initialization" blockType="command" 
    export function SPI_Init(parameter: any, block: any) {
       Generator.addImport("import img_spi_v2"); 
       Generator.addCode(`img_spi_v2.Init()`); 
   }

    //###Start||启动
    //% block="Start" blockType="command"
    export function Start(parameter: any, block: any) {
        Generator.addImport("import img_spi_v2");
        Generator.addCode(`img_spi_v2.Robots_mode(0x02)`);   
        Generator.addCode(`time.sleep_ms(100);`);
    }

    //###Stop||停止
    //% block="Stop" blockType="command"
    export function Stop(): void {
        Generator.addImport("import img_spi_v2");
        Generator.addCode(`img_spi_v2.Robots_mode(0x01)`);  
    }
    
    // //####Reset||复位
    // //% block="Reset" blockType="command"
    // export function Reset(): void{
          
    // }

    //###Stand||站立 
    //% block="Stand" blockType="command"
    export function Stand(): void{
        Generator.addImport("import img_spi_v2");
        Generator.addCode(`img_spi_v2.Robots_mode(0x07)`);  
    }

    //####Hight||高度
    //% block="Height[H]" blockType="command"
    //%H.shadow="range" H.params.min=0 H.params.max=10 H.defl=10
    export function Height(parameter: any, block: any){
        let h = parameter.H.code;

        Generator.addImport("import img_spi_v2");
        Generator.addCode(`img_spi_v2.Robots_High(${h});`); 
        Generator.addCode(`time.sleep_ms(500);`);
    }

    //###Gait||步态
    //% block="Gait[G]" blockType="command"
    //% G.shadow="dropdown" G.options="gait" G.defl="gait.Trot"
    export function Gait(parameter: any, block: any) {
        let g = parameter.G.code;

        Generator.addImport("import img_spi_v2");
        Generator.addCode(`img_spi_v2.Robots_mode(${g});`); 
    }

    //###Action group||动作组
    //% block="Action_group[GROUP]State[STATE]" blockType="command"
    //% GROUP.shadow="dropdown" GROUP.options="Choice" GROUP.defl="Choice.Enable"
    //% STATE.shadow="dropdown" STATE.options="Actions" STATE.defl="Actions.Enable"
    export function Action(parameter: any, block: any): void{
        let group = parameter.GROUP.code;
        let state = parameter.STATE.code;

        Generator.addImport("import img_spi_v2");
        Generator.addCode(`img_spi_v2.Robots_Action(${group},${state});`); 
    }
    
    //###Before and after movement direction and speed||前后运动方向与速度
    //% block="Control[FOR]Speed[V1]" blockType="command"
    //% FOR.shadow="dropdown" FOR.options="Mov_dir" FOR.defl="Mov_dir.0"
    //% V1.shadow="range" V1.params.min=0 V1.params.max=14 V1.defl=0
    export function movement(parameter: any, block: any) {
        let ffor = parameter.FOR.code;    
        let v1 = parameter.V1.code;
       
        Generator.addImport("import img_spi_v2");
        if(ffor == 0){
        Generator.addCode(`img_spi_v2.Robots_Xspeed(${v1*0.1});`);
        }
        else if(ffor == 1){
            Generator.addCode(`img_spi_v2.Robots_Xspeed(-${v1*0.1});`);
        }
        else if(ffor == 2){
            Generator.addCode(`img_spi_v2.Robots_Zspeed(${v1*0.1});`);
        }
        else if(ffor == 3){
            Generator.addCode(`img_spi_v2.Robots_Zspeed(-${v1*0.1});`);
        }
        else if(ffor == 4){
            Generator.addCode(`img_spi_v2.Robots_Yspeed(-${v1*0.1});`);
        }
        else if(ffor == 5){
            Generator.addCode(`img_spi_v2.Robots_Yspeed(${v1*0.1});`);
        }
   }

    //###Control angle||控制角度
    //% block="Control[SWAY]angle[ANGLE1]" blockType="command"
    //% SWAY.shadow="dropdown" SWAY.options="Mov_ang" SWAY.defl="Mov_ang.0"
    //% ANGLE1.shadow="range" ANGLE1.params.min=0 ANGLE1.params.max=14 ANGLE1.defl=0
    export function Control_angle(parameter: any, block: any): void{
        let sway = parameter.SWAY.code;    
        let angle1 = parameter.ANGLE1.code;
 
        Generator.addImport("import img_spi_v2");
        if(sway == 0){
        Generator.addCode(`img_spi_v2.Robots_Yangle(${angle1*0.1});`);
        }
        else if(sway == 1){
            Generator.addCode(`img_spi_v2.Robots_Yangle(-${angle1*0.1});`);
        }
        else if(sway == 2){
            Generator.addCode(`img_spi_v2.Robots_Xangle(${angle1*0.1});`);
        }
        else if(sway == 3){
            Generator.addCode(`img_spi_v2.Robots_Xangle(-${angle1*0.1});`);
        }
        else if(sway == 4){
            Generator.addCode(`img_spi_v2.Robots_Zangle(${angle1*0.1});`);
        }
        else if(sway == 5){
            Generator.addCode(`img_spi_v2.Robots_Zangle(-${angle1*0.1});`);
        }
    }
    
    // //###Steering gear control||舵机控制
    // //% block="Steering_gear_control the[ge]PWM[num]Speed[v2]millisecond" blockType="command"
    // //% ge.shadow="dropdown" ge.options="PWM" ge.defl="PWM.0"
    // //% num.shadow="range" num.params.min=0 num.params.max=2500 num.defl=0
    // //% v2.shadow="range" v2.params.min=0 v2.params.max=9 v2.defl=0
    // export function Steering_gear(parameter: any, block: any): void{

    // }

    //####Get the data||获取数据
    //% block="Get the data" blockType="command"
    export function get_data(block: any): void{
        Generator.addImport("import img_spi_v2");
        Generator.addCode(`datareturn = img_spi_v2.Robots_Sta();`);
        Generator.addCode(`time.sleep_ms(1000);`);
        Generator.addCode(`print(datareturn)`);
        Generator.addCode(`print(datareturn[0])`);
    }

    //###Returns action status information||返回动作组状态信息
    //% block="Returns action group status information" blockType="reporter"
    export function Action_Status(block: any): void{
        Generator.addImport("import img_spi_v2");
        Generator.addCode(["datareturn[1]", Generator.ORDER_UNARY_POSTFIX]);
    }

    //###Return  hexadecimal number||返回状态信息
    //% block="Returns the status information of the robot itself" blockType="reporter"
    export function Status(block: any): void{
        Generator.addImport("import img_spi_v2");
        Generator.addCode(["datareturn[0]", Generator.ORDER_UNARY_POSTFIX]);

    }

}
