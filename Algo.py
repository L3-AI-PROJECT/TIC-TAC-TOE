class Algo:
    @staticmethod
    def elagage_minimax(chess, a, b, isMax):
        pos = []
        for i in range(9):
            if chess[i] == 0:
                pos.append(i)
        
        result = [0, 0]
        for po in pos:
            if isMax:
                chess[po] = 1
            else:
                chess[po] = -1
            
            value = Algo.get_result(chess)
            
            if value == 2:
                value = Algo.elagage_minimax(chess, a, b, not isMax)[1]
            
            if isMax:
                if a < value:
                    a = value
                    result[0] = po
            else:
                if b > value:
                    b = value
                    result[0] = po
            
            chess[po] = 0
            
            if b <= a:
                break
        
        if isMax:
            result[1] = a
        else:
            result[1] = b
        return result
    
    @staticmethod
    def get_result(chess):
        if chess[0] == chess[1] == chess[2] and chess[0] != 0:
            return chess[0]
        elif chess[3] == chess[4] == chess[5] and chess[3] != 0:
            return chess[3]
        elif chess[6] == chess[7] == chess[8] and chess[6] != 0:
            return chess[6]
        elif chess[0] == chess[3] == chess[6] and chess[0] != 0:
            return chess[0]
        elif chess[1] == chess[4] == chess[7] and chess[1] != 0:
            return chess[1]
        elif chess[2] == chess[5] == chess[8] and chess[2] != 0:
            return chess[2]
        elif chess[0] == chess[4] == chess[8] and chess[0] != 0:
            return chess[0]
        elif chess[2] == chess[4] == chess[6] and chess[2] != 0:
            return chess[2]
        
        for i in range(9):
            if chess[i] == 0:
                return 2
        
        return 0

