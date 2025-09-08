from .crud_operations import CarCRUD
from .models import Car
from .database import mongodb_connection

def display_menu():
    print("\n" + "="*50)
    print("🚗 SISTEMA DE GERENCIAMENTO - CONCESSIONÁRIA")
    print("="*50)
    print("1. Cadastrar novo carro")
    print("2. Listar todos os carros")
    print("3. Buscar carro por ID")
    print("4. Atualizar carro")
    print("5. Excluir carro")
    print("6. Estatísticas do estoque")
    print("0. Sair")
    print("="*50)

def get_car_data():
    print("\n📝 Cadastro de Novo Carro:")
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    ano = int(input("Ano: "))
    cor = input("Cor: ").strip()
    preco = float(input("Preço: R$ "))
    quilometragem = int(input("Quilometragem: "))
    combustivel = input("Combustível: ").strip()
    cambio = input("Câmbio: ").strip()
    portas = int(input("Portas: "))
    placa = input("Placa: ").strip().upper()
    
    return Car(
        marca=marca,
        modelo=modelo,
        ano=ano,
        cor=cor,
        preco=preco,
        quilometragem=quilometragem,
        combustivel=combustivel,
        cambio=cambio,
        portas=portas,
        placa=placa
    )

def main():
    crud = CarCRUD()
    
    while True:
        display_menu()
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            try:
                car = get_car_data()
                car_id = crud.create_car(car)
                print(f"✅ Carro cadastrado com sucesso! ID: {car_id}")
            except Exception as e:
                print(f"❌ Erro ao cadastrar carro: {e}")
        
        elif choice == '2':
            cars = crud.read_all_cars()
            print(f"\n📋 Total de carros: {len(cars)}")
            for i, car in enumerate(cars, 1):
                print(f"\n{i}. {car}")
                print("-" * 40)
        
        elif choice == '3':
            car_id = input("Digite o ID do carro: ").strip()
            car = crud.read_car_by_id(car_id)
            if car:
                print(f"\n🔍 Carro encontrado:\n{car}")
            else:
                print("❌ Carro não encontrado!")
        
        elif choice == '4':
            car_id = input("Digite o ID do carro para atualizar: ").strip()
            car = crud.read_car_by_id(car_id)
            if car:
                print(f"Carro atual: {car}")
                new_price = input("Novo preço (deixe em branco para manter): ").strip()
                if new_price:
                    try:
                        updated_car = crud.update_car(car_id, {"preco": float(new_price)})
                        if updated_car:
                            print(f"✅ Carro atualizado:\n{updated_car}")
                    except:
                        print("❌ Erro ao atualizar carro!")
            else:
                print("❌ Carro não encontrado!")
        
        elif choice == '5':
            car_id = input("Digite o ID do carro para excluir: ").strip()
            if crud.delete_car(car_id):
                print("✅ Carro excluído com sucesso!")
            else:
                print("❌ Erro ao excluir carro!")
        
        elif choice == '6':
            stats = crud.get_stats()
            print("\n📊 Estatísticas do Estoque:")
            print(f"Total de carros: {stats['total_cars']}")
            print(f"Carros disponíveis: {stats['available_cars']}")
            print(f"Carros vendidos: {stats['sold_cars']}")
        
        elif choice == '0':
            print("👋 Saindo do sistema...")
            mongodb_connection.close_connection()
            break
        
        else:
            print("❌ Opção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()