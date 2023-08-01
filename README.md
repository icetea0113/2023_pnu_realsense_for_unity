# 2023_pnu_realsense_for_unity

Unity main 파일에서 invoke를 받으면 적절한 작업을 수행할 RealSenseManager 파일 생성 함. -> 정확하게 수행하는지는 확인되지 않음.


start_record.py -> realsense camera의 RGB image data와 depth image data를 bag파일로 저장함. (정상적으로 저장됨을 확인)


extract_data.py -> .bag 파일을 통해 2D RGB image를 다시 만든 뒤 mediapipe를 통해 skeleton data를 생성함. 그 후 얻은 skeleton data의 x,y 좌표를 이용해 depth image의 z 값을 추출해서 timestamp와 엮어주고 txt파일에 기록해줌.(여기까지 정상적으로 저장됨을 확인. 아직 스켈레톤 데이터가 정확하게 입혀져있는지는 확인 못함) 하지만 신체가 전부 나오지 않으면 mediapipe가 신체를 추측해서 x, y값을 추정함. 그로 인해 z값이 정상적으로 나오지 않는 현상이 있음.
