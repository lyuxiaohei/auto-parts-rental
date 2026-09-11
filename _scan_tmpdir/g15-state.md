# G15 执行状态（抗断续跑）
T0=done 备份 backup-f01-20260911 + 状态文件建立（前置：并发封锁经道远现场解除；M:N 存档 86675fc）
T1=done .wrap max-width 1280→880 assert=1
T2=done 主SVG收编：分隔线x2×9、右对齐注记×7、决策框×3(B1 3行/L3 3行/L4)、T1长侧注拆行、适用注记×2、T2注记×3、F1注记拆行
T3=done 主图例两行(5+4)+主viewBox 0 0 880 2184
T4=done 支SVG：S1切4+3、S5切3+3、S2/S3/S4+44、S5+44、S6+76、图例+108、viewBox 0 0 880 846（S6注记落点偏差见失败清单）
T5=done g15_gates.py 四门首轮 ALL PASS（溢出0/重叠0/href92=text3137字一致/grep 残留0）
T6=done 审计113页死链0/JS0 + g14 diff 既有108页新增0 + mobile 5页0/0（门5 PASS）
T7=done 截图 g15-f01-after.png + 三件套回写 + 提交 fca99e8（工作）+本批（回写）
